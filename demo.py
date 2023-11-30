from winedge import Card, Evaluator

hand = [
    Card.new('5s'),
    Card.new('Ah')
]

board = [
    Card.new('2h'),
    Card.new('2s'),
    Card.new('Jc'),
    Card.new('Kh'),
    Card.new('Qc')
]

evaluator = Evaluator()

rankclass = evaluator.class_to_string(evaluator.get_rank_class(evaluator.evaluate(hand, board)))
rankperc = evaluator.get_rank_percentage(evaluator.evaluate(hand, board))

print("Rank class for your hand is: %s" % rankclass)
print("The hand strength is: %f" % rankperc)


