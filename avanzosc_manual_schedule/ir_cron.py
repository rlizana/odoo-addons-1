# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

import calendar
import time
import logging
import threading
import psycopg2
from datetime import datetime
from dateutil.relativedelta import relativedelta

import netsvc
import openerp
import pooler
import tools
from openerp.cron import WAKE_UP_NOW
from osv import fields, osv
from tools import DEFAULT_SERVER_DATETIME_FORMAT
from tools.safe_eval import safe_eval as eval
from tools.translate import _

_logger = logging.getLogger(__name__)

# This variable can be set by a signal handler to stop the infinite loop in
# ir_cron._run()
quit_signal_received = False

# This variable can be checked to know if ir_cron._run() is processing a job or
# sleeping.
job_in_progress = True


class ir_cron(osv.osv):
    _name="ir.cron"
    _inherit="ir.cron"
    
    def run_jobs_manual(self, id_list):
        # TODO remove 'check' argument from addons/base_action_rule/base_action_rule.py
        """ Process the cron jobs by spawning worker threads.

        This selects in database all the jobs that should be processed. It then
        tries to lock each of them and, if it succeeds, spawns a thread to run
        the cron job (if it doesn't succeed, it means the job was already
        locked to be taken care of by another thread).

        The cursor used to lock the job in database is given to the worker
        thread (which has to close it itself).

        """
        db = self.pool.db
        cr = db.cursor()
        db_name = db.dbname
        try:
            print id_list
            jobs = {} # mapping job ids to jobs for all jobs being processed.
            now = datetime.now() 
            # Careful to compare timestamps with 'UTC' - everything is UTC as of v6.1.
            cr.execute("""SELECT * FROM ir_cron
                          WHERE numbercall != 0
                              AND active AND id in %s
                          ORDER BY priority""", (tuple(id_list),))
            for job in cr.dictfetchall():
                print job
                if not openerp.cron.get_thread_slots():
                    break
                jobs[job['id']] = job

                task_cr = db.cursor()
                try:
                    # Try to grab an exclusive lock on the job row from within the task transaction
                    acquired_lock = False
                    task_cr.execute("""SELECT *
                                       FROM ir_cron
                                       WHERE id=%s
                                       FOR UPDATE NOWAIT""",
                                   (job['id'],), log_exceptions=False)
                    acquired_lock = True
                except psycopg2.OperationalError, e:
                    if e.pgcode == '55P03':
                        # Class 55: Object not in prerequisite state; 55P03: lock_not_available
                        _logger.debug('Another process/thread is already busy executing job `%s`, skipping it.', job['name'])
                        continue
                    else:
                        # Unexpected OperationalError
                        raise
                finally:
                    if not acquired_lock:
                        # we're exiting due to an exception while acquiring the lot
                        task_cr.close()

                # Got the lock on the job row, now spawn a thread to execute it in the transaction with the lock
                task_thread = threading.Thread(target=self._run_job, name=job['name'], args=(task_cr, job, now))
                # force non-daemon task threads (the runner thread must be daemon, and this property is inherited by default)
                task_thread.setDaemon(False)
                openerp.cron.take_thread_slot()
                task_thread.start()
                _logger.debug('Cron execution thread for job `%s` spawned', job['name'])

            # Find next earliest job ignoring currently processed jobs (by this and other cron threads)
            find_next_time_query = """SELECT min(nextcall) AS min_next_call
                                      FROM ir_cron WHERE numbercall != 0 AND active""" 
            if jobs:
                cr.execute(find_next_time_query + " AND id NOT IN %s", (tuple(jobs.keys()),))
            else:
                cr.execute(find_next_time_query)
            next_call = cr.dictfetchone()['min_next_call']

            if next_call:
                next_call = calendar.timegm(time.strptime(next_call, DEFAULT_SERVER_DATETIME_FORMAT))
            else:
                # no matching cron job found in database, re-schedule arbitrarily in 1 day,
                # this delay will likely be modified when running jobs complete their tasks
                next_call = time.time() + (24*3600)

            openerp.cron.schedule_wakeup(next_call, db_name)

        except Exception, ex:
            _logger.warning('Exception in cron:', exc_info=True)

        finally:
            cr.commit()
            cr.close()

ir_cron()