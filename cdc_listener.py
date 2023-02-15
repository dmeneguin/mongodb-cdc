import pymongo

db = pymongo.MongoClient('mongodb://mongo1:27017/')
db = db.test
print('conectando...')
try:
    resume_token = None
    #pipeline = [{'$match': {'operationType': 'insert'}}]
    with db.jorge.watch() as stream:
        for insert_change in stream:
            print(insert_change)
            resume_token = stream.resume_token
except pymongo.errors.PyMongoError as e:
    # The ChangeStream encountered an unrecoverable error or the
    # resume attempt failed to recreate the cursor.
    if resume_token is None:
        # There is no usable resume token because there was a
        # failure during ChangeStream initialization.
        print(e)
    else:
        # Use the interrupted ChangeStream's resume token to create
        # a new ChangeStream. The new stream will continue from the
        # last seen insert change without missing any events.
        print('??????')
        with db.collection.watch(
                pipeline, resume_after=resume_token) as stream:
            for insert_change in stream:
                print(insert_change)