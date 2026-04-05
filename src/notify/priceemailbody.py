class PriceEmailBody:

    def __init__(self, prices):
        self.prices = prices

    def build(self):
        instruments = list(self.prices.keys())
        dates = sorted({v[0] for v in self.prices.values() if v is not None}, reverse=True)

        header = ' | '.join(['Date'] + instruments)
        rows = [header]
        if dates:
            for date in dates:
                row = [date] + [
                    str(self.prices[i][1]) if self.prices[i] is not None and self.prices[i][0] == date else 'N/A'
                    for i in instruments
                ]
                rows.append(' | '.join(row))
        else:
            rows.append(' | '.join(['N/A'] * (len(instruments) + 1)))
        return '\n'.join(rows)

    def build_html(self):
        instruments = list(self.prices.keys())
        dates = sorted({v[0] for v in self.prices.values() if v is not None}, reverse=True)

        th_style = 'border: 1px solid #ccc; padding: 6px 12px; background-color: #f2f2f2; text-align: left;'
        td_style = 'border: 1px solid #ccc; padding: 6px 12px;'

        header_cells = ''.join(f'<th style="{th_style}">{col}</th>' for col in ['Date'] + instruments)
        header_row = f'<tr>{header_cells}</tr>'

        if dates:
            data_rows = ''
            for date in dates:
                cells = [date] + [
                    str(self.prices[i][1]) if self.prices[i] is not None and self.prices[i][0] == date else 'N/A'
                    for i in instruments
                ]
                data_rows += '<tr>' + ''.join(f'<td style="{td_style}">{c}</td>' for c in cells) + '</tr>'
        else:
            na_cells = ''.join(f'<td style="{td_style}">N/A</td>' for _ in range(len(instruments) + 1))
            data_rows = f'<tr>{na_cells}</tr>'

        return f'<html><body><table style="border-collapse: collapse;">{header_row}{data_rows}</table></body></html>'

    def build_terminal(self):
        from tabulate import tabulate
        instruments = list(self.prices.keys())
        dates = sorted({v[0] for v in self.prices.values() if v is not None}, reverse=True)
        if dates:
            rows = [
                [date] + [
                    self.prices[i][1] if self.prices[i] is not None and self.prices[i][0] == date else 'N/A'
                    for i in instruments
                ]
                for date in dates
            ]
        else:
            rows = [['N/A'] * (len(instruments) + 1)]
        return tabulate(rows, headers=['Date'] + instruments, tablefmt='fancy_grid')

    def most_recent_date(self):
        return max((v[0] for v in self.prices.values() if v is not None), default='N/A')