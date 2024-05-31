import graph


def main():
    g = graph.Graph.make_from_file('graphs/c4.txt')
    print(g.skew_zero_forcing(set(('A'))))


if __name__ == '__main__':
    main()