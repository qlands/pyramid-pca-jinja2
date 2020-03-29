from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from ..models import MyModel


def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == "one").first()
    except DBAPIError:
        return Response(db_err_msg, content_type="text/plain", status=500)

    return {"one": one, "project": "PCA Example"}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pcaexample_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
