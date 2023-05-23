int evaluate_omaha_cards(int, int, int, int, int, int, int, int, int);
int evaluate_cards(int c1, int c2, int c3, int c4, int c5, int h1, int h2, int h3, int h4) {
    return evaluate_omaha_cards(c1, c2, c3, c4, c5, h1, h2, h3, h4);
}
