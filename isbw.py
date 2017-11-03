import sys
import os
import json
import datetime

import dateutil.parser

CONFIG_FILEPATH = os.path.join(os.path.expanduser("~"), ".isbw")


def format_ppd(project_data):
    if (project_data[1] == None):
        return "[%s]" % project_data[2]
    else:
        return "%.2f" % project_data[1]

def get_total(data):
    total = 0.0
    for project_data in data:
        if (project_data[1] != None and project_data[1] >= 0.0):
            total += project_data[1]

    return format_ppd((None, total))

def get_data():
    if not os.path.exists(CONFIG_FILEPATH):
        sys.exit(1)

    try:
        data = json.load(open(CONFIG_FILEPATH, 'r'))
        data = data["projects"]
    except:
        sys.exit(1)

    output = []

    today = dateutil.parser.parse(str(datetime.date.today()))
    for project_data in data:
        try:
            name = project_data["name"]
            due_date = dateutil.parser.parse(project_data["due"])
            days_left = (due_date - today).days
            pages_remaining = project_data["total"] - project_data["written"]
            pages_per_day = float(pages_remaining) / float(days_left)

            if (days_left < 0):
                output.append((name, None, "overdue"))
            elif (pages_per_day < 0):
                output.append((name, None, "finished"))
            else:
                output.append((name, pages_per_day))
        except ValueError:
            output.append((name, None, "error"))

    return output


def print_ascii(output):
    output_table = []

    total_ppd = get_total(output)

    if len(output) == 0 or total_ppd == 0.0:
        output_table.append(["I don't need to be writing!", ""])
    else:
        output_table.append(["Pages", "Project"])
        output_table.append(["-----", "-------"])
        for project in output:
            row = [format_ppd(project), project[0]]
            output_table.append(row)
        output_table.append(["", ""])
        output_table.append([total_ppd, "Total"])

        col_widths = [0, 0]
        for output_data in output_table:
            for i in xrange(len(col_widths)):
                if len(output_data[i]) > col_widths[i]:
                    col_widths[i] = len(output_data[i])

        for row in output_table:
            print "{0: ^{width0}}  {1: ^{width1}}".format(row[0], row[1], width0=col_widths[0], width1=col_widths[1])


def print_html(output):
    total_ppd = get_total(output)

    if len(output) == 0 or total_ppd == 0.0:
        print "<h1>I don't need to be writing!</h1>"
    else:
        print "<table>"
        print "\t<tr class=\"header\"><th>Pages Per Day</th><th>Project</th></tr>"
        for project in output:
            print "\t<tr class=\"project\"><td class=\"ppd\">%s</td><td class=\"label\">%s</td></tr>" % (format_ppd(project), project[0])
        print "\t<tr class=\"total\"><td class=\"ppd\">%s</td><td class=\"label\">Total</td></tr>" % (total_ppd)
        print "</table>"


def main():
    output = get_data()

    if "--ascii" in sys.argv or len(sys.argv) == 1:
        print_ascii(output)

    elif "--html" in sys.argv:
        print_html(output)


if __name__ == '__main__':
    main()

