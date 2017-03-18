# -*- coding: utf-8 -*-

from argparse import ArgumentParser

parser = ArgumentParser(description = "Ein Taschenrechner")
parser.add_argument("-o", "--operation", dest="operation",
                    default="plus", help="Rechenoperation")
parser.add_argument("operanden", metavar="Operand", type=float,
                    nargs="+", help="Operanden")
parser.add_argument("-i", "--integer", dest="type",
                    action="store_const", const=int, default=float,
                    help="Ganzzahlige Berechnung")

args = parser.parse_args()

calc = {
"plus" : lambda a,b : a+b,
"minus" : lambda a,b : a-b,
"mal" : lambda a,b : a*b,
"durch" : lambda a,b : a/b
}

op = args.operation
if op in calc:
    res = 0 if op in ("plus", "minus") else 1
    for z in args.operanden:
        res = calc[op](res, args.type(z))
        print("Ergebnis: ", res)
else:
    parser.error("{} ist keine gültige Operation".format(op))

# konsequentes Nutzen der KW-Args... z.B. fuer HIlfeseite
# -h, --help