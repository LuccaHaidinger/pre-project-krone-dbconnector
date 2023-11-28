from mysql.connector import connect, Error
from torchtext.data import Field, TabularDataset, BucketIterator

try:
    conn = connect(
        user = 'htl',
        password = 'mew-Pz58QF',
        host = '192.168.239.53',
        port = 3306,
        database = 'wp')

    cursor = conn.cursor()
    query = 'SELECT post_title FROM wp_posts'
    cursor.execute(query)
    data = cursor.fetchall()

    for r in data:
        print(r)
    cursor.close()
    conn.close()
except Error as err:
    print('Error message: ' + err.msg)

# Define the fields
TEXT = Field(sequential=True, tokenize='spacy', lower=False)
LABEL = Field(sequential=False, use_vocab=False)

# Create a TabularDataset
fields = [('text', TEXT), ('label', LABEL)]  # Adjust the column names accordingly
examples = [({'text': row[0]}, row[1]) for row in data]
train_data = TabularDataset(path=None, format='json', fields=fields, examples=examples)

# Build the vocabulary
TEXT.build_vocab(train_data)

# Create a BucketIterator for batching
train_iterator = BucketIterator(
    train_data,
    batch_size=64,
    sort_key=lambda x: len(x.text),
    shuffle=True
)