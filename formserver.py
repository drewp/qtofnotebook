import csv
import json
import os
import bottle

RESPONSES = 'out.csv'

def fillSelectionDirs(question):
    """
    If the question wants a dir listing for its replies, replace its
    select list with strings.
    """
    resp = question['response']
    if 'select' in resp and isinstance(resp['select'], dict):
        if 'listdir' in resp['select']:
            resp['select'] = os.listdir(resp['select']['listdir'])

@bottle.get('/form.json')
def formjson():
    filename = 'form.json'
    try:
        obj = json.load(open(filename))
    except ValueError as e:
        bottle.abort(500, 'In %s: %s' % (os.path.abspath(filename), e))

    for question in obj['questions']:
        fillSelectionDirs(question)
        
    bottle.response.set_header('Content-Type', 'application/json')
    return json.dumps(obj)

@bottle.get('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static')

@bottle.get('/')
def index():
    return bottle.static_file('index.html', root='.')

def foldOthers(row):
    """
    Edit the row, collapsing all 'foo' and 'foo-other' keys into just
    'foo'.
    """
    for k, v in row.items():
        if k.endswith('-other'):
            root = k[:-len('-other')]
            if row.get(root, '') == '(other)':
                row[root] = v
            del row[k]

def filledOutputRow(headings, row):
    """
    Return a row list for the given row dict. headings will be
    extended if necessary.
    """
    positionedRow = [None] * len(headings)
    for k, v in sorted(row.items()):
        try:
            column = headings.index(k)
        except ValueError:
            headings.append(k)
            positionedRow.append(None)
            column = headings.index(k)
        positionedRow[column] = v
    return positionedRow

def rebuildCsv(newHeadings, newRow):
    """
    Append newRow to the CSV file, and also replace its headings
    (first row).
    """
    with open(RESPONSES, 'r') as rf:
        allRows = list(csv.reader(rf))
    if len(allRows) < 1:
        allRows.append(newHeadings)
    else:
        allRows[0] = newHeadings
    allRows.append(newRow)
    safelyRewriteCsv(allRows)
    
def safelyRewriteCsv(allRows):
    outPath = RESPONSES + '_temp'
    with open(outPath, 'w') as wf:
        writer = csv.writer(wf)
        writer.writerows(allRows)
    os.rename(outPath, RESPONSES)
    
def appendCsvRow(positionedRow):
    with open(RESPONSES, 'a') as wf:
        writer = csv.writer(wf)
        writer.writerow(positionedRow)
    
@bottle.post('/results')
def results():
    row = {}
    for k, vs in bottle.request.POST.dict.items():
        row[k] = row.get(k, vs[0])

    foldOthers(row)
    try:
        headings = csv.reader(open(RESPONSES)).next()
    except (IOError, StopIteration):
        headings = []
    originalHeadings = headings[:]
    positionedRow = filledOutputRow(headings, row)
    if headings != originalHeadings:
        rebuildCsv(headings, positionedRow)
    else:
        appendCsvRow(positionedRow)
        
bottle.run(port=8080)
