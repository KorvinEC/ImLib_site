import datetime

from app.init_app import app, db, manager
from app.models import User, Image, Tag, Image_Tag, Library, Library_image
import os

#Image functions ---------------------------------------------------------------

def add_image(name):
    image = Image.query.filter(Image.name == name).first()
    if not image:
        image = Image(name = name)
        db.session.add(image)
        db.session.commit()
    return image

def add_image_to_libDB(library_id, image_id):
    image = Library_image.query.filter(Library_image.library_id == library_id,
                                       Library_image.image_id == image_id
                                       ).first()
    if not image:
        image = Library_image(library_id = library_id,
                              image_id = image_id,
                              )
        db.session.add(image)
        db.session.commit()
    return image

def delete_image_from_libDB(image_id, library_id):
    image_in_lib = Library_image.query.filter(Library_image.library_id == library_id,
                                       Library_image.image_id == image_id
                                       ).first()
    if image_in_lib:
        db.session.delete(image_in_lib)
        db.session.commit()
        return 1
    return None 

def get_image_id_name(image_id):
    image = Image.query.filter(Image.id == image_id).first()
    if image:
        file_exctension = os.path.splitext(image.name)
        image_id_name = str(image.id) + file_exctension[1]
        return image_id_name
    return None

def get_image(image_id):
    image = Image.query.filter(Image.id == image_id).first()
    return image

def delete_imageDB(image_id):
    image = Image.query.filter(Image.id == image_id).first()
    if image:
        db.session.delete(image)
        db.session.commit()
        return 1
    return None

def delete_image_file(image_id):
    filename = get_image_id_name(image_id)
    imageurl = os.path.join(app.config['UPLOAD_FOLDER'],
                            filename
                            )
    os.remove(imageurl)
    if not os.path.isfile(imageurl):
        return 1
    return None

def get_images_by_tag(tag_id):
    images = Image_Tag.query.filter(Image_Tag.tag_id == tag_id).all()
    return images

def get_images_from_library(library_id, tags_names=None):
    images_id = Library_image.query.filter(Library_image.library_id == library_id).all()
    if tags_names:
        tag_obejects = []
        for tag_name in tags_names:
            query = Tag.query.filter(Tag.tag == tag_name).first()
            if not query: continue
            tag_obejects.append(query)
        images_id_copy = images_id
        images_id = []
        for image_id in images_id_copy:
            for tag_object in tag_obejects:
                query = Image_Tag.query.filter(Image_Tag.image_id == image_id.image_id,
                                               Image_Tag.tag_id == tag_object.id
                                               ).first()
                if not query: continue
                images_id.append(query)
    if images_id:
        image_objects = []
        for image_id in images_id:
            image_objects.append(Image.query.filter(Image.id == image_id.image_id).first())
        return image_objects
    return None

def get_image_libraries(image_id, user_id):
    image_in_libraries = Library_image.query.filter(Library_image.image_id == image_id).all()
    libraries = db.session.query(Library).filter(Library.user_id == user_id).all()
    for image_in_library in image_in_libraries:
        for library in libraries:
            if library.id == image_in_library.library_id:
                libraries.remove(library)
    return libraries

def get_image_libs_to_delete(image_id):
    image_in_libraries = Library_image.query.filter(Library_image.image_id == image_id).all()
    libraries = []
    for image_in_library in image_in_libraries:
        query = db.session.query(Library).filter(Library.id == image_in_library.library_id).first()
        if query.name == 'Gallery':
            continue
        libraries.append(query)
    return libraries

def change_image_name(image_id, image_name):
    image = Image.query.filter_by(id = image_id).first()
    if image:
        file_exctension = os.path.splitext(image.name)
        image.name = image_name + file_exctension[1]
        db.session.commit()
        return 1
    return None

#Library functions -------------------------------------------------------------

def find_library(user_id, library_name):
    library = Library.query.filter(Library.user_id == user_id,
                                   Library.name == library_name
                                   ).first()
    return library

def add_library(library_name, parent_library, user_id):
    librarydb = Library.query.filter(Library.name == library_name,
                                     Library.parent == parent_library,
                                     Library.user_id == user_id
                                     ).first()
    if not librarydb:
        librarydb = Library(name = library_name,
                            parent = parent_library,
                            user_id = user_id
                            )
        db.session.add(librarydb)
        db.session.commit()
    return librarydb

def get_library(library_id):
    libraries = Library.query.filter(Library.id == library_id).first()
    return libraries    

def get_all_libraries_from_library(user_id, parent_library):
    libraries = Library.query.filter(Library.user_id == user_id,
                                     Library.parent == parent_library
                                     ).all()
    return libraries

def delete_libraryDB(library_id):
    library = Library.query.filter(Library.id == library_id).first()
    if library:
        db.session.delete(library)
        db.session.commit()
        return 1
    return None

def change_library_name(library_id, library_new_name):
    new_library = Library.query.filter(Library.name == library_new_name).first()
    if not new_library:
        library = Library.query.filter(Library.id == library_id).first()
        if library:
            library.name = library_new_name
            db.session.commit()
            return 1
        return None
    return 1

#Tag functions -----------------------------------------------------------------

def add_tag(adding_tag):
    tagdb = Tag.query.filter(Tag.tag == adding_tag).first()
    if not tagdb:
        tagdb = Tag(tag = adding_tag)
        db.session.add(tagdb)
        db.session.commit()
    return tagdb

def get_tags(image_id, user_id):
    tags_on_image = Image_Tag.query.filter(Image_Tag.image_id == image_id,
                                           Image_Tag.user_id == user_id
                                           ).all()
    if tags_on_image:
        clipped_tags = []
        for tags in tags_on_image:
            clipped_tags.append(Tag.query.filter(Tag.id == tags.tag_id).first())
        return clipped_tags
    return None

def add_tag_to_image(image_id, tag_id, user_id):
    image_tag = Image_Tag.query.filter(Image_Tag.image_id == image_id,
                                       Image_Tag.tag_id == tag_id,
                                       Image_Tag.user_id == user_id
                                       ).first()
    if not image_tag:
        image_tag = Image_Tag(image_id = image_id,
                              tag_id = tag_id,
                              user_id = user_id
                              )
        db.session.add(image_tag)
        db.session.commit()

def delete_tag_on_image(tag_id, image_id, user_id):
    tag = Image_Tag.query.filter(Image_Tag.image_id == image_id,
                                 Image_Tag.tag_id == tag_id,
                                 Image_Tag.user_id == user_id
                                 ).first()
    if tag:
        db.session.delete(tag)
        db.session.commit()
        return 1
    return None

def delete_tags(image_id, user_id):
    tags = Image_Tag.query.filter(Image_Tag.image_id == image_id,
                                           Image_Tag.user_id == user_id
                                           ).all()
    if tags:
        for tag in tags:
            db.session.delete(tag)
            db.session.commit()
        return 1
    return None

def change_tag_on_image(tag_id, tag_name):
    new_tag = Tag.query.filter(Tag.tag == tag_name).first()
    if not new_tag:
        tag = Tag.query.filter(Tag.id == tag_id).first()
        if tag:
            tag.tag = tag_name
            db.session.commit()
            return 1
        return None
    return 1