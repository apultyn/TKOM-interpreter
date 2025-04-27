import src.parser.parser_objects as po
import src.parser.parser_util as pu


def test_assignments(make_parser):
    parser = make_parser("a = 10;")

    assert parser.parse_program() == po.Program(
        [
            po.AssignmentStmt(
                po.Identifier("a"),
                pu.AssignmentType.NORMAL,
                po.SimpleTypeExpr(pu.SimpleLiteralType.INT, 10),
            )
        ]
    )
