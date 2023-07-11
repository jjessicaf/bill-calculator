# Jessica Fu
# Description: Calculates bill based on number of people and who has what items

from flask import Flask, redirect, render_template, request, session, url_for
import os
from werkzeug.utils import secure_filename
from collections import OrderedDict
import re
import db_actions
import app_ocr
from uvicorn.workers import UvicornWorker


UPLOAD_FOLDER = os.path.join('static', 'uploads')
app = Flask(__name__, template_folder='templates', static_folder='static')
app_name = "Bill Calculator"
# to store uploaded images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


nums = [i for i in range(11)] # up to 10 people
items = OrderedDict() # item name : qty, price

# overall TO-DOS:
# - go back button from options -- will clear the data
# - host on github under projects

@app.route("/")
def start():
    """
    start page that asks for number of people, allows you to set their names, the image of items, and the tip amount
    :return: renders start.html
    """
    type = "none" if ('num_people' not in session or session['num_people'] == 0) else "block"
    peeps = (-1) if 'num_people' not in session else session['num_people']
    tip = 0 if 'tip' not in session else session['tip']
    ne = False if 'ne' not in session else session['ne']
    session['ne'] = False
    ie = False if 'ie' not in session else session['ie']
    session['ie'] = False
    # bill = '' if 'bill_img_path' not in session else session['bill_img_path']

    return render_template("start.html", default_display=type, message=app_name, nums=nums, nums_error=ne, last=peeps, img_error=ie, tip=tip)

@app.route("/submit_data", methods=["POST"])
def check_data():
    """
    checks to make sure all needed values have been submitted: number of people, tip, image
    :return: if entered all the info is right, render options, else go back to start
    """
    if request.method == "POST":
        session['num_people'] = int(request.form['num_people'])
        # make it so that it highlights the missing section with red
        bill_img = request.files['bill_img']
        filename = secure_filename(bill_img.filename)
        session['tip'] = request.form['tip']

        to_redirect = False
        if 'num_people' not in request.form or request.form['num_people'] == '0':
            session['ne'] = True
            to_redirect = True
        if 'bill_img' not in request.files or len(filename) == 0:
            session['ie'] = True
            to_redirect = True
        else:
            session['img_name'] = db_actions.upload_image(bill_img)
            if not session['img_name']:
                session['ie'] = True
            #bill_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #session['bill_img_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if 'tip' not in request.form:
            to_redirect = True

        if to_redirect:
            return redirect(url_for("start"))

        session['names'] = []
        for i in range(session['num_people']):
            if ("name"+str(i)) in request.form:
                session['names'].append(request.form["name" + str(i)].lower())
        # reference: https://thinkinfi.com/upload-and-display-image-in-flask-python/
        received, tax = process_img(session['img_name'])
        if tax != "":
            session['tax'] = float(tax)
        if not received:
            print("invalid bill!")
            del session['img_name']
            #del session['bill_img_path']
            # say the bill is invalid
            return redirect(url_for('start'))
        return redirect(url_for('options'))
    return redirect(url_for('start'))

@app.route("/options")
def options():
    """
    choose who has which items
    :return: renders options.html
    """
    # reference: https://web.dev/drag-and-drop/
    if not items:
        # error message
        return redirect(url_for('start'))
    # for the jinja: https://stackoverflow.com/questions/25373154/how-to-iterate-through-a-list-of-dictionaries-in-jinja-template

    request_tax = False
    if 'tax' not in session:
        request_tax = True

    return render_template("options.html", names=session['names'], items=items, request_tax=request_tax)

@app.route("/assign_items", methods=["POST"])
def item_assigner():
    """
    calculates based on who has what items
    :return: the results page or error if didn't work
    """
    if request.method == "POST":
        assignment = {}
        remaining_items = [item for item in items] # for items that aren't assigned
        assigned_items = {key: 0 for key in items}
        # get all the data from options.html and store in lists
        for person in session['names']:
            if person in request.form:
                all_items = request.form[person].split(', ')
                all_items = list(filter(lambda x: x != '', all_items))
                success = True
                assignment[person] = [] # list of lists
                for i in all_items:
                    if i not in request.form:
                        success = False
                        break
                    if i in remaining_items:
                        remaining_items.remove(i)
                    item_name = request.form[i]
                    qty_name = i + " " + str(items[i][0])
                    if qty_name not in request.form:
                        success = False
                        break
                    item_qty = request.form[qty_name]
                    price_name = i + " " + str(items[i][1])
                    if price_name not in request.form:
                        success = False
                        break
                    item_price = request.form[price_name]
                    assignment[person].append([item_name, float(item_price), int(item_qty)])
                    if item_name not in assigned_items: # if the item_name has been changed
                        del assigned_items[i]
                        assigned_items[item_name] = 0
                        items[item_name] = items.pop(i)
                    items[item_name] = [item_qty, item_price]
                    assigned_items[item_name] += 1

                if not success:
                    print(":(")
                    # to-do: error handling

        session['assignment'] = assignment
        # items that aren't assigned are distributed amongst all participants
        for item in remaining_items:
            if assigned_items[item] == 0:
                item_name = request.form[item]
                qty_name = item + " " + str(items[item][0])
                if qty_name not in request.form:
                    success = False
                    break
                item_qty = request.form[qty_name]
                price_name = item + " " + str(items[item][1])
                if price_name not in request.form:
                    success = False
                    break
                item_price = request.form[price_name]
                for person in assignment:
                    assignment[person].append([item_name, float(item_price), int(item_qty)])
                if item_name not in assigned_items:
                    del assigned_items[item]
                    items[item_name] = items.pop(item)
                items[item_name] = [item_qty, item_price]
                assigned_items[item_name] = session['num_people']

        if not success:
            print(":(")
            # to-do: error handling

        session['assigned_items'] = assigned_items

        return redirect(url_for('results'))

@app.route("/results")
def results():
    """
    displays the results by person
    :return:
    """
    message = "Bill Results"
    # bill calculator
    totals = bill_calculator() # person : amount

    # offer recalculate

    return render_template("results.html", message=message, totals=totals, assignment=session['assignment'])

@app.route("/recalculate", methods=["POST"])
def recalculate():
    return redirect(url_for('options'))

@app.route("/share", methods=["POST"])
def share():
    # have shares for each individual, and also overall
    return redirect(url_for('results'))

def process_img(img_path):
    """
    takes the bill image and returns the items on the image
    :param img_path: path to image
    :return: boolean success or failure, tax percent/amount
    """
    text = app_ocr.img_to_text(img_path)
    text = re.sub(r'.(?=00)', '.', text)
    text = text.lower()
    start = max(text.find('qty'), text.find('amount'), text.find('price'))
    text = text[start:]

    tax = ""
    subtotal = ""
    end = -1
    is_quanity = False

    lines = text.split('\n')
    for line in lines:
        if line.find('subtotal') > -1:
            subtotal = re.sub(r'\D', '', line).strip()
            continue
        if line.find('tax') > -1:
            if line.find('$') > -1:
                is_quanity = True
            tax = re.sub(r'\D', '', line).strip()
            continue
        if line.find('total') > -1:
            end = lines.index(line)
            break
        content = line.split(' ')
        price = -1.0
        name = ""
        qty = 1
        for i in range(len(content)):
            idx = content[i].find('.')
            if idx > -1 and i > 0:
                price = float(re.sub(r'[^0-9.]', '', content[i][0:idx + 2]).strip()) # remove any non-numeric chars
                has_qty = False
                try:
                    float(content[i - 1])
                    has_qty = True
                except ValueError:
                    has_qty = False
                n = i - 1 if has_qty else i
                qty = int(content[n]) if has_qty else qty
                temp = '{} ' * n
                name = [temp.format(*word) for word in zip(*[iter(content)] * i)][0]
                name = re.sub(r'[^a-zA-Z\s]', '', name).strip()
                break
        if price < 0 or name == "":
            continue
        items[name] = [qty, price]

    if tax == "" and end != -1:
        for i in range(end, len(lines)):
            if lines[i].find('tax') > -1:
                if lines[i].find('$') > -1:
                    is_quanity = True
                tax = re.sub('[a-zA-Z]', '', lines[i]).strip()
                break
    if tax != "":
        if is_quanity:
            try:
                tax = float(tax)
                subtotal = float(subtotal)
                tax = tax/subtotal
            except ValueError:
                tax = ""
        else: # is percent
            try:
                tax = float(tax)
                tax = tax / 100
            except ValueError:
                tax = ""

    # delete the images
    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, file))

    if len(items) == 0:
        return False, tax

    return True, tax

def bill_calculator():
    """
    calculates based on who has what items
    :return: dict of person and total
    """
    totals = {person: 0.0 for person in session['names']}

    tax = 1.0963 # san mateo tax :(
    if 'tax' in session: # tax must be a percent
        tax = 1 + float(session['tax'])

    tip = 1.0 if session['tip'] == 0 else (1.0 + float(session['tip'])/100)

    # equation: sum(price*qty)*tax*tip
    for person in session['assignment']:
        curr = 0.0
        for item in session['assignment'][person]:
            # [name, price, qty]
            ppl = session['assigned_items'][item[0]]
            curr += (item[1]*item[2]/ppl)
        curr = curr * tax * tip
        totals[person] = round(curr, 2)

    return totals


# main entrypoint
# runs app
app.secret_key = os.urandom(16)
if __name__ == "__main__":
    app.run()