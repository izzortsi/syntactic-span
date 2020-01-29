N = ["S"] #terminal symbols
E = ["a", "b"] #nonterminal symbols

function P1(str) # maps each ocurrence of the terminal symbol S into the word "aBs", yielding one new string per ocurrence

    ematch = eachmatch(r"S", str)
    matchs = collect(ematch)
    nstr_list = Vector{String}(undef, 0)

    for m in matchs
        push!(nstr_list, str[1:m.offset-1]*replace(str[m.offset:end], m.match => "aSb", count=1))
    end

    return nstr_list

end

function P2(str) # maps each ocurrence of the terminal symbol S into the word "bSa", yielding one new string per ocurrence

    ematch = eachmatch(r"S", str)
    matchs = collect(ematch)
    nstr_list = Vector{String}(undef, 0)

    for m in matchs
        push!(nstr_list, str[1:m.offset-1]*replace(str[m.offset:end], m.match => "bSa", count=1))
    end

    return nstr_list

end

function P3(str) # maps each ocurrence of the terminal symbol S into the word "ab", yielding one new string per ocurrence

    ematch = eachmatch(r"S", str)
    matchs = collect(ematch)
    nstr_list = Vector{String}(undef, 0)

    for m in matchs
        push!(nstr_list, str[1:m.offset-1]*replace(str[m.offset:end], m.match => "ab", count=1))
    end

    return nstr_list

end

function T1(str1, str2)
    ocs1 = occursin(r"(a|b)(a|b)", str1) | occursin(r"(a|b)(a|b)", str2)
    ocs2 = occursin(r"(a|b)S(a|b)", str1) | occursin(r"(a|b)S(a|b)", str2)
    if (ocs1*ocs2 == true) & (str1[1]==str2[1]) & (str1[end]==str2[end])
        return (str1[1]^2) * "S" * (str1[end]^2)
    end
end

function T2(str)
    len = length(str)
    if len%2==0 & !occursin(r"S", str)
        return str[1:len÷2]*"S"*str[len÷2:end]
    end
end


function main()
    

str = "SSS"

P1(str)

str1 = "bSa"
str2 = "ba"

T1(str1, str2)

str = "SSSS"

T2(str)
