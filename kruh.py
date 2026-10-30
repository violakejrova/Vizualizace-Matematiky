from manim import *
PI_symbol = MathTypst("pi", font_size=36)

def cz(x, mist=4):
    return f"{x:.{mist}f}".replace(".", ",")

class ObsahKruhu(Scene):
    def construct(self):
        r = 1 
        k = 2.2     # zvětšení na obrazovce
        self.nadpis = Text("Obsah kruhu", font_size=40).to_edge(UP)
        rtext = Text("r = 1", font_size=32).to_corner(UL)
        self.play(Write(self.nadpis), Write(rtext))

        pocty = [8, 16, 1024]
        for n in pocty:
            self.faze(n, r, k, posledni=(n == pocty[-1]))

    def faze(self, n, r, k, posledni):
        R = r * k
        theta = TAU / n
        tloustka = 1 if n <= 32 else 0

        sektory = VGroup(*[
            AnnularSector(inner_radius=0, outer_radius=R, angle=theta,
                          start_angle=i * theta,
                          fill_color=BLUE if i % 2 == 0 else TEAL,
                          fill_opacity=0.8,
                          stroke_color=WHITE, stroke_width=tloustka)
            for i in range(n)
        ])
        pocet = Text(f"počet výsečí: {n}", font_size=32).next_to(self.nadpis, DOWN)

        self.play(FadeIn(sektory), Write(pocet), run_time=2)
        self.wait(2)

        d = R * np.tan(theta / 2)
        uhly, posuny = [], []
        for i in range(n):
            stred = i * theta + theta / 2
            cil = PI / 2 if i % 2 == 0 else -PI / 2
            uhly.append((cil - stred + PI) % TAU - PI)
            x = (i - (n - 1) / 2) * d
            y = -R / 2 if i % 2 == 0 else R / 2
            posuny.append(np.array([x, y, 0]))

        if n <= 32:
            self.play(*[Rotate(s, angle=uhly[i], about_point=ORIGIN)
                        for i, s in enumerate(sektory)], run_time=4)
            self.wait(1)
            self.play(*[s.animate.shift(posuny[i])
                        for i, s in enumerate(sektory)], run_time=4)
        else:
            hotove = VGroup(*[
                s.copy().rotate(uhly[i], about_point=ORIGIN).shift(posuny[i])
                for i, s in enumerate(sektory)
            ])
            self.play(FadeOut(sektory), FadeIn(hotove), run_time=4)
            sektory = hotove
        self.wait(1)

        # popisky rozměrů obdélníku (u každé fáze)
        b_v = Brace(sektory, LEFT)
        t_v = Text("r", font_size=30).next_to(b_v, LEFT)
        b_s = Brace(sektory, DOWN)
        t_s = Text("polovina obvodu", font_size=28).next_to(b_s, DOWN)
        self.play(GrowFromCenter(b_v), Write(t_v),
                  GrowFromCenter(b_s), Write(t_s))
        self.wait(1)

        # počítání
        sirka = n * np.sin(PI / n) * r
        vypocet = Text(
            f"šířka ≈ {cz(sirka)}   výška = 1   obsah ≈ {cz(sirka)}",
            font_size=30).to_edge(DOWN)
        self.play(Write(vypocet))
        self.wait(3)

        if not posledni:
            self.play(FadeOut(sektory), FadeOut(vypocet), FadeOut(pocet),
                      FadeOut(b_v), FadeOut(t_v), FadeOut(b_s), FadeOut(t_s))
            return

        # závěr
        

        t_s2 = VGroup(
            Text("polovina obvodu = ", font_size=28),
            PI_symbol.copy(),
            Text(" ≈ 3,1416", font_size=28)
        ).arrange(RIGHT, buff=0.05).next_to(b_s, DOWN)

        self.play(FadeOut(vypocet), Transform(t_s, t_s2))
        self.wait(2)

        vzorec = MathTypst(
            'text("Obsah") = pi dot r dot r = pi dot r^2',
            font_size=40
        ).to_edge(UP)

        self.play(Transform(self.nadpis, vzorec), FadeOut(pocet))
        self.wait(4)
