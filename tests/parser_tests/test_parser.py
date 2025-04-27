import io

import src.parser.parser_objects as po
import src.parser.parser_util as pu

from src.parser.parser import Parser
from src.lexer.lexer import Lexer


def test_assignments():
    source = io.StringIO("a = 10; b += ")
    lexer = Lexer(source)
    parser = Parser(lexer=lexer)

    assert parser.parse_program() == po.Program(
        [
            po.AssignmentStmt(
                po.Identifier("a"),
                pu.AssignmentType.NORMAL,
                po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 10),
            )
        ]
    )
