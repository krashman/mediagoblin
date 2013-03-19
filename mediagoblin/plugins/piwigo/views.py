# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2013 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from werkzeug.exceptions import MethodNotAllowed
from werkzeug.wrappers import BaseResponse

from mediagoblin.meddleware.csrf import csrf_exempt
from mediagoblin.tools.response import render_404
from .tools import CmdTable, PwgNamedArray, response_xml


_log = logging.getLogger(__name__)


@CmdTable("pwg.session.login", True)
def pwg_login(request):
    username = request.form.get("username")
    password = request.form.get("password")
    _log.info("Login for %r/%r...", username, password)
    _log.warn("login: %s %r %r", request.method,
                  request.args, request.form)
    return True


@CmdTable("pwg.session.logout")
def pwg_logout(request):
    _log.info("Logout")
    return True


@CmdTable("pwg.getVersion")
def pwg_getversion(request):
    _log.info("getversion")
    return "piwigo 2.5.0"


@CmdTable("pwg.categories.getList")
def pwg_categories_getList(request):
    catlist = ({'id': -29711},)
    return {
          'categories': PwgNamedArray(
            catlist,
            'category',
            (
              'id',
              'url',
              'nb_images',
              'total_nb_images',
              'nb_categories',
              'date_last',
              'max_date_last',
            )
          )
        }


@csrf_exempt
def ws_php(request):
    if request.method not in ("GET", "POST"):
        _log.error("Method %r not supported", request.method)
        raise MethodNotAllowed()

    func = CmdTable.find_func(request)
    if not func:
        _log.warn("wsphp: Unhandled %s %r %r", request.method,
                  request.args, request.form)
        return render_404(request)

    result = func(request)

    if isinstance(result, BaseResponse):
        return result

    return response_xml(result)