import io
import csv
from typing import Optional, Annotated
from fastapi import FastAPI, Depends, Request
from fastapi.responses import StreamingResponse
from app.database import Database
from app.models import PageModel, ClientModel


def db_lifespan(app):
    app.database = Database(source="data.csv")
    yield
    app.database.close()

app = FastAPI(lifespan=db_lifespan)


@app.get("/clients")
def get_clients(request: Request, 
                page: int = 1, 
                limit: int = 1000)-> PageModel:
    rows = request.app.database.fetch_rows(page, limit)
    count = request.app.database.rows_count
    pages_num = count//limit + 1 if count%limit > 0 else count//limit
    return PageModel(
        total_pages=pages_num,
        page_number=page,
        data=[ClientModel.from_list(row) for row in rows]
    )


@app.get("/download")
def download_clients(request: Request, 
                     filters: Annotated[Optional[dict], Depends(Database.get_filters)]):
    data = request.app.database.fetch_rows(filters=filters)
    if data: 
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['category', 'firstname', 'lastname', 'email', 'gender', 'birthDate'])
        writer.writerows(row[1:] for row in data)
        output.seek(0)  # go back to the beginning of the file
        return StreamingResponse(io.BytesIO(output.read().encode()), 
                                media_type="text/csv", 
                                headers={"Content-Disposition": "attachment;filename=clients.csv"}
                                )
    return {"message": "No clients found"}