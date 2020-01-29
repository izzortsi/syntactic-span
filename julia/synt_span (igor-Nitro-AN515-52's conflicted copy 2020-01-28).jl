N = ["S"] #terminal symbols
E = ["a", "b"] #nonterminal symbols

function prod1(s)
    matchs = eachmatch(r"S", s)
end

macro p_str(s)
    matchs = eachmatch(r"S", s)

    map((x)->replace(r"S", x))
end

p"S"
prod1("S")

nS = replace(N[1]^2, "S" => E[1]*E[2], count=1)
nS = replace(nS, "S" => E[1]*E[2], count=1)

p"S"

matchs = eachmatch(r"S", N[1]^3)
matchs
map((x)->replace(r"S", x), matchs)

for m in matchs
    println(m.match)
end
