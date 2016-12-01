
function(s, pop)

    require "struct"

    local bytes_read = 1
    local bytes_to_unpack = 1
    local max = string.len(s) / bytes_to_unpack
    local total_bytes = 1
    local negation = 2 ^ (bytes_to_unpack * 8) - 1
    local fmt = 'I'..bytes_to_unpack
    local totals = 0
    while bytes_read <= max do
        if totals == pop then break end
        local d
        d, bytes_read = struct.unpack(fmt, s, bytes_read)
        local ones = {}
        while d ~= 0 do
            -- Calculate position of 1
            local d_ones = d
            local inner_ones = 0
            while bit.band(d_ones, 1) == 0 do
                inner_ones = inner_ones + 1
                d_ones = bit.rshift(d_ones, 1)
            end
            ones[#ones + 1] = ((bytes_read - 1) * 8) - 1 - inner_ones
            -- positions[#positions + 1] = ((bytes_read - 1) * 8) - 1 - inner_ones
            d = bit.band(d, d - 1)
            totals = totals + 1
        end
        table.sort(ones)
        for i, one in ipairs(ones) do coroutine.yield(one) end
    end
end
