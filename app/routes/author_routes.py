from flask import Blueprint, abort, make_response, request, Response

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()

    try:
        new_author = Author.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_author)
    db.session.commit()

    return new_author.to_dict(), 201

@bp.get("")
def get_all_author():
    query = db.select(Author)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    author = db.session.scalars(query.order_by(Author.id))
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    authors_response = []
    for author in authors:
        authors_response.append(book.to_dict())
    return authors_response

@bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Book, book_id)

    return author.to_dict()
