import sys
import re
from random import randint


def convert_class_to_full_css(class_converter, content, variable, all_vars):
    cl = class_converter(variable)
    cl_child = cl + "-ch > *"
    cl_children_self = cl + "-ch-all"
    cl_children = cl + "-ch-all *"
    for child in all_vars:
        if child is not variable:
            formatted = class_converter(child)
            cl_children += ":not({})".format(formatted)
            cl_children += ":not({})".format(formatted + "-ch-all")
            cl_children += ":not({})".format(formatted + "-ch")
            cl_child += ":not({})".format(formatted)
            cl_child += ":not({})".format(formatted + "-ch-all")

    ret = cl + ",\n" + cl_child + ",\n" + cl_children_self + ",\n" + cl_children + " {\n"
    ret += "\t" + content + "\n"
    ret += "}"
    return ret


def var_to_fg_class(var):
    return ".col-" + var[2:]


def var_to_bg_class(var):
    return ".col-" + var[2:] + "-bg"


def convert_to_fg_css(variable, all_vars):
    content = "color: var({}) !important;".format(variable)
    return convert_class_to_full_css(var_to_fg_class, content, variable, variables)


def convert_to_bg_css(variable, all_vars):
    content = "background-color: var({}) !important;".format(variable)
    return convert_class_to_full_css(var_to_bg_class, content, variable, variables)


if __name__ == '__main__':
    file_name = input("filename: ")

    variables = []
    css_var = input("Add variable: ")

    pattern = re.compile(r"--[A-Za-z](-?[A-Za-z0-9]+)*")

    while css_var[:2] == "--":
        if css_var in variables:
            print("variable already in list, try again or end the adding "
                  "by passing anything that doesn't start with --")
        else:
            if re.match(pattern, css_var):
                variables.append(css_var)
            else:
                print("Invalid variable name, try again or end the adding by "
                      "passing anything that doesn't start with --")
        css_var = input("Add variable: ").lower()

    if len(variables) == 0:
        print("cant generate with 0 variables, exiting")
        sys.exit()

    print("dump variables")
    for i, v in enumerate(variables, start=1):
        print('[{}]: {}'.format(i, v))

    confirm = input("Generate with these variables? [Y/y]es / [N/n]o: ")
    if confirm != "Y" and confirm != "y":
        print("Ok, stopping")
        sys.exit()
    print("Continuing...")

    file = '* {\n'

    for v in variables:
        file += '\t{}: rgb({},{},{});\n'.format(v, randint(0, 255), randint(0, 255), randint(0, 255))

    file += '}\n\n'

    for v in variables:
        file += convert_to_fg_css(v, variables) + "\n\n"
        file += convert_to_bg_css(v, variables) + "\n\n"

    print(file)

    f = open("./res/" + file_name, 'w')
    f.write(file)
    f.close()
