from manim import *

# Vertikální formát
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 6
config.frame_height = 10.67

PI_symbol = MathTypst("pi", font_size=36)

STRED = UP * 0.8   # posun celého obrazce nahoru

PISMO_UVOD = 28
PISMO_VZOREC = 48

# závěr: barva čísel, která se mění, a poloměry, které se postupně ukážou
BARVA_CISEL = YELLOW
POLOMERY = [0.5, 1.3, 1]


def cz(x, mist=4):
    return f"{x:.{mist}f}".replace(".", ",")


def fmt(x):
    return f"{x:g}".replace(".", ",")


def tn(x):
    # číslo pro Typst; desetinné číslo s čárkou musí být v uvozovkách
    s = fmt(x)
    return f'"{s}"' if "," in s else s


def blok(*radky, velikost=24):
    # několik řádků textu pod sebou
    return VGroup(*[Text(r, font_size=velikost) for r in radky]).arrange(DOWN, buff=0.15)


class ObsahKruhu(Scene):
    def construct(self):
        r = 1
        k = 1.1

        self.uvod(r * k)

        self.nadpis = Text("Obsah kruhu", font_size=32).to_edge(UP)
        rtext = Text("r = 1", font_size=24).next_to(self.nadpis, DOWN, buff=0.15)

        self.play(Write(self.nadpis), Write(rtext))

        pocty = [8, 16, 1024]
        for n in pocty:
            self.faze(n, r, k, rtext, posledni=(n == pocty[-1]))

    def uvod(self, R):
        # Otázka nahoře
        otazka = blok(
            "Napadlo vás někdy,",
            "proč se obsah kruhu",
            "počítá zrovna takhle?",
            velikost=PISMO_UVOD,
        ).to_edge(UP, buff=0.85)

        # Kruh s poloměrem
        kruh = Circle(radius=R, color=WHITE, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.6).move_to(STRED)
        polomer = Line(STRED, STRED + RIGHT * R, color=YELLOW, stroke_width=4)
        r_pop = Text("r", font_size=24, color=YELLOW).next_to(polomer, UP, buff=0.1)

        # Vzorec složený z částí, aby šlo pracovat se samotným pí
        s_lev = MathTypst("S =", font_size=PISMO_VZOREC)
        s_pi = MathTypst("pi", font_size=PISMO_VZOREC)
        s_r = MathTypst("r^2", font_size=PISMO_VZOREC)
        vzorec = VGroup(s_lev, s_pi, s_r).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        vzorec.next_to(kruh, DOWN, buff=0.6)

        self.play(Write(otazka), run_time=2)
        self.play(DrawBorderThenFill(kruh), Create(polomer), Write(r_pop), run_time=2)
        self.play(Write(vzorec))
        self.wait(1)

        # pí se zvětší, zežloutne a blikne
        self.play(s_pi.animate.scale(1.6).set_color(YELLOW), run_time=0.85)
        self.play(Indicate(s_pi, color=YELLOW, scale_factor=1.3))
        self.play(Indicate(s_pi, color=YELLOW, scale_factor=1.3))

        proc = VGroup(
            Text("Proč je tam zrovna", font_size=PISMO_UVOD),
            MathTypst("pi", font_size=36),
            Text("?", font_size=PISMO_UVOD),
        ).arrange(RIGHT, buff=0.12).next_to(vzorec, DOWN, buff=0.6)
        self.play(Write(proc))
        self.wait(1)

        hodnota = VGroup(
            MathTypst("pi", font_size=36),
            Text("= 3,14159265...", font_size=PISMO_UVOD),
        ).arrange(RIGHT, buff=0.15).set_color(YELLOW).next_to(proc, DOWN, buff=0.4)
        self.play(TransformFromCopy(s_pi, hodnota))
        self.wait(1)

        trojka = blok(
            "Vždyť je to jen",
            "taková \"fancy trojka\"...",
            velikost=26,
        ).next_to(hodnota, DOWN, buff=0.4)
        self.play(FadeIn(trojka, shift=UP * 0.2))
        self.wait(2)

        # Přechod ke krájení
        prechod = Text("Pojďme kruh rozkrájet!", font_size=30, color=YELLOW).move_to(otazka)
        self.play(
            s_pi.animate.scale(1 / 1.6).set_color(WHITE),
            FadeOut(proc), FadeOut(hodnota), FadeOut(trojka),
            FadeTransform(otazka, prechod),
        )
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in (prechod, kruh, polomer, r_pop, vzorec)])
        self.wait(0.5)

    def faze(self, n, r, k, rtext, posledni):
        R = r * k
        theta = TAU / n
        tloustka = 1 if n <= 32 else 0

        sektory = VGroup(*[
            AnnularSector(
                inner_radius=0,
                outer_radius=R,
                angle=theta,
                start_angle=i * theta,
                fill_color=BLUE if i % 2 == 0 else GOLD,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=tloustka
            )
            for i in range(n)
        ])
        sektory.shift(STRED)   # špičky všech výsečí jsou teď v bodě STRED

        pocet = Text(f"počet výsečí: {n}", font_size=24).next_to(rtext, DOWN, buff=0.15)

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
            self.play(
                *[Rotate(s, angle=uhly[i], about_point=STRED)
                  for i, s in enumerate(sektory)],
                run_time=4
            )
            self.wait(1)

            self.play(
                *[s.animate.shift(posuny[i]) for i, s in enumerate(sektory)],
                run_time=4
            )
        else:
            hotove = VGroup(*[
                s.copy().rotate(uhly[i], about_point=STRED).shift(posuny[i])
                for i, s in enumerate(sektory)
            ])
            self.play(FadeOut(sektory), FadeIn(hotove), run_time=4)
            sektory = hotove

        self.wait(1)

        # Zvýraznění obdélníku
        obrys = SurroundingRectangle(sektory, buff=0, color=YELLOW, stroke_width=5)
        self.play(Create(obrys), run_time=1.5)
        self.play(Indicate(obrys, color=YELLOW, scale_factor=1.05))

        # Popisky rozměrů obdélníku
        b_v = Brace(sektory, LEFT)
        t_v = Text("r", font_size=22).next_to(b_v, LEFT)

        b_s = Brace(sektory, DOWN)
        t_s = Text("polovina obvodu", font_size=22).next_to(b_s, DOWN)

        self.play(GrowFromCenter(b_v), Write(t_v),
                  GrowFromCenter(b_s), Write(t_s))
        self.wait(1)

        # Vzorec pro obsah obdélníku
        vzorec_obd = Text("obsah obdélníku = šířka · výška",
                          font_size=24, color=YELLOW).next_to(t_s, DOWN, buff=0.45)
        self.play(Write(vzorec_obd))
        self.wait(1.5)

        # Počítání, každá hodnota na vlastním řádku
        sirka = n * np.sin(PI / n) * r
        vypocet = blok(
            f"šířka ≈ {cz(sirka)}",
            "výška = 1",
            f"obsah ≈ {cz(sirka)} · 1 = {cz(sirka)}",
        ).next_to(vzorec_obd, DOWN, buff=0.35)

        self.play(Write(vypocet))
        self.wait(3)

        if not posledni:
            self.play(
                FadeOut(sektory), FadeOut(obrys), FadeOut(vzorec_obd),
                FadeOut(vypocet), FadeOut(pocet),
                FadeOut(b_v), FadeOut(t_v), FadeOut(b_s), FadeOut(t_s)
            )
            return

        # Závěr
        t_s2 = VGroup(
            Text("polovina obvodu = ", font_size=24),
            PI_symbol.copy(),
            Text(" ≈ 3,1416", font_size=24)
        ).arrange(RIGHT, buff=0.15).next_to(b_s, DOWN)
        self.play(FadeOut(vypocet), FadeOut(vzorec_obd), Transform(t_s, t_s2))
        self.wait(2)

        # obsah kruhu = obsah obdélníku = šířka · výška = pí·r · r = pí r^2
        vzorec = VGroup(
            Text("Obsah kruhu = obsah obdélníku", font_size=24),
            Text("= šířka · výška", font_size=24, color=YELLOW),
            MathTypst("= pi r dot r = pi r^2", font_size=36),
        ).arrange(DOWN, buff=0.2).next_to(t_s, DOWN, buff=0.4)

        self.play(FadeIn(vzorec[0]), FadeOut(pocet), FadeOut(rtext))
        self.wait(1)
        self.play(Write(vzorec[1]), Indicate(obrys, color=YELLOW))
        self.wait(1)
        self.play(Write(vzorec[2]))
        self.wait(4)

        self.zaver_pomer(sektory, obrys, [vzorec, b_v, t_v, b_s, t_s], k)

    def telo_obdelniku(self, r, u, barvy):
        # jednobarevný obdélník: šířka pi*r, výška r (v měřítku u), žlutý rám
        sirka, vyska = PI * r * u, r * u
        vypln = Rectangle(width=sirka, height=vyska, fill_color=barvy[0],
                          fill_opacity=0.85, stroke_width=0).move_to(STRED)
        ram = Rectangle(width=sirka, height=vyska, stroke_color=YELLOW,
                        stroke_width=5, fill_opacity=0).move_to(STRED)
        return VGroup(vypln, ram)

    def obdelnik(self, r, u, barvy):
        # obdélník s popisky stran; čísla jsou zvlášť, aby se dala jen "probliknout"
        telo = self.telo_obdelniku(r, u, barvy)
        b_v = Brace(telo, LEFT)
        t_v = Text(fmt(r), font_size=22, color=BARVA_CISEL).next_to(b_v, LEFT, buff=0.1)
        b_s = Brace(telo, DOWN)
        t_s = VGroup(
            Text(fmt(r), font_size=22, color=BARVA_CISEL),
            MathTypst("pi", font_size=30),
        ).arrange(RIGHT, buff=0.05).next_to(b_s, DOWN, buff=0.1)
        skupina = VGroup(telo, b_v, t_v, b_s, t_s)
        skupina.staticke = [telo, b_v, b_s, t_s[1]]
        skupina.cisla = [t_v, t_s[0]]
        return skupina

    def radky_pomeru(self, r):
        # S = r . r pi = r^2 pi   a   S / r^2 = (r^2 pi) / r^2 = pi
        vel = 30

        def cislo(x):
            return Text(fmt(x), font_size=26, color=BARVA_CISEL)

        radek1 = VGroup(
            MathTypst("S =", font_size=vel),
            cislo(r),
            MathTypst("dot", font_size=vel),
            cislo(r),
            MathTypst("pi =", font_size=vel),
            cislo(r * r),
            MathTypst("pi", font_size=vel),
        ).arrange(RIGHT, buff=0.1)

        citatel = VGroup(cislo(r * r), MathTypst("pi", font_size=vel)).arrange(RIGHT, buff=0.05)
        jmenovatel = cislo(r * r)
        cara = Line(ORIGIN, RIGHT * (citatel.width + 0.1), stroke_width=2)
        zlomek = VGroup(citatel, cara, jmenovatel).arrange(DOWN, buff=0.1)
        radek2 = VGroup(
            MathTypst("S / r^2 =", font_size=vel),
            zlomek,
            MathTypst("= pi", font_size=vel),
        ).arrange(RIGHT, buff=0.12)

        skupina = VGroup(radek1, radek2).arrange(DOWN, buff=0.25).move_to(DOWN * 3.2)
        skupina.staticke = [radek1[0], radek1[2], radek1[4], radek1[6],
                            citatel[1], cara, radek2[0], radek2[2]]
        skupina.cisla = [radek1[1], radek1[3], radek1[5], citatel[0], jmenovatel]
        return skupina

    def zmena(self, stare, nove):
        # statické části se jen posunou, čísla se vymění (prolnou) bez psaní
        return (
            [ReplacementTransform(s, n) for s, n in zip(stare.staticke, nove.staticke)]
            + [FadeOut(c) for c in stare.cisla]
            + [FadeIn(c) for c in nove.cisla]
        )

    def zaver_pomer(self, sektory, obrys, stare, u):
        # barvy převzít z výsečí, aby obdélník ladil s tím, co bylo před ním
        barvy = (sektory[0].get_fill_color(), sektory[1].get_fill_color())

        # Výseče zmizí, pod žlutým rámem zůstane dvoubarevný obdélník
        telo = self.telo_obdelniku(1, u, barvy)
        self.play(
            FadeOut(sektory),
            *[FadeOut(m) for m in stare],
            FadeIn(telo[0]),
        )
        self.remove(obrys)
        self.add(telo)
        self.wait(0.5)

        # Rovnice S = pi r^2 po částech
        vel = 44
        pS = MathTypst("S", font_size=vel)
        pEq = MathTypst("=", font_size=vel)
        pPi = MathTypst("pi", font_size=vel)
        pR = MathTypst("r^2", font_size=vel)
        rovnice = VGroup(pS, pEq, pPi, pR).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.85)
        self.play(Write(rovnice))
        self.wait(1)

        # Vyjádření pi: písmenka se přesunou do tvaru pi = S / r^2
        cara = Line(LEFT * 0.35, RIGHT * 0.35, stroke_width=3)
        zlomek = VGroup(pS.copy(), cara, pR.copy()).arrange(DOWN, buff=0.12)
        cil = VGroup(pPi.copy(), pEq.copy(), zlomek).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.85)
        self.play(
            pPi.animate.move_to(cil[0]),
            pEq.animate.move_to(cil[1]),
            pS.animate.move_to(zlomek[0]),
            pR.animate.move_to(zlomek[2]),
            run_time=2,
        )
        self.play(Create(cara))
        self.wait(1)

        vysvetleni = VGroup(
            Text("Nezáleží na tom, jak velký kruh je.", font_size=24),
            VGroup(
                MathTypst("pi", font_size=32),
                Text("je vždy poměr obsahu a", font_size=24),
                MathTypst("r^2", font_size=32),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 3.2)
        self.play(Write(vysvetleni))
        self.wait(2)

        # Obdélník dostane popisky stran (stejná velikost jako dosud, r = 1)
        skupina = self.obdelnik(1, u, barvy)
        self.remove(telo)
        self.add(skupina[0])
        self.play(*[FadeIn(m) for m in skupina[1:]])
        self.add(skupina)
        self.wait(1)

        # Výpočet poměru se napíše jen jednou
        pomer = self.radky_pomeru(1)
        self.play(FadeOut(vysvetleni), Write(pomer))
        self.wait(2)

        # Pak se mění jen velikost obdélníku a čísla probliknou
        for r in POLOMERY:
            nova_skupina = self.obdelnik(r, u, barvy)
            novy_pomer = self.radky_pomeru(r)
            self.play(
                *self.zmena(skupina, nova_skupina),
                *self.zmena(pomer, novy_pomer),
                run_time=1.5,
            )
            skupina, pomer = nova_skupina, novy_pomer
            self.add(skupina, pomer)
            self.play(
                *[Indicate(c, color=WHITE, scale_factor=1.3)
                  for c in skupina.cisla + pomer.cisla],
                run_time=0.7,
            )
            self.wait(2)

        # Závěr
        zaver = VGroup(
            Text("Ať je kruh jakkoli velký,", font_size=26),
            VGroup(
                MathTypst("pi", font_size=36),
                Text("tam bude vždycky.", font_size=26),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 3.2)
        self.play(FadeOut(pomer), FadeIn(zaver), Indicate(pPi, color=YELLOW, scale_factor=1.4))
        self.wait(4)
