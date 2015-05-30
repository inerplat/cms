#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2010-2013 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2015 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2012 Matteo Boscariol <boscarim@hotmail.com>
# Copyright © 2012-2014 Luca Wehrstedt <luca.wehrstedt@gmail.com>
# Copyright © 2014 Artem Iglikov <artem.iglikov@gmail.com>
# Copyright © 2014 Fabian Gundlach <320pointsguy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Announcement-related handlers for AWS for a specific contest.

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import tornado.web

from cms.db import Contest, Announcement
from cmscommon.datetime import make_datetime

from .base import BaseHandler, try_commit


class AddAnnouncementHandler(BaseHandler):
    """Called to actually add an announcement

    """
    def post(self, contest_id):
        self.contest = self.safe_get_item(Contest, contest_id)

        subject = self.get_argument("subject", "")
        text = self.get_argument("text", "")
        if subject != "":
            ann = Announcement(make_datetime(), subject, text,
                               contest=self.contest)
            self.sql_session.add(ann)
            try_commit(self.sql_session, self)
        self.redirect("/contest/%s/announcements" % contest_id)


class RemoveAnnouncementHandler(BaseHandler):
    """Called to remove an announcement.

    """
    def get(self, contest_id, ann_id):
        ann = self.safe_get_item(Announcement, ann_id)
        self.contest = self.safe_get_item(Contest, contest_id)

        # Protect against URLs providing incompatible parameters.
        if self.contest is not ann.contest:
            raise tornado.web.HTTPError(404)

        self.sql_session.delete(ann)

        try_commit(self.sql_session, self)
        self.redirect("/contest/%s/announcements" % contest_id)
