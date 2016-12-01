
function(s, pop)
    require "struct"
    -- Start reading byte 1
    local bytes_read = 1
    local bytes_to_unpack = 1
    local max = string.len(s) / bytes_to_unpack
    local negation = 2 ^ (bytes_to_unpack * 8) - 1
    local fmt = 'I'..bytes_to_unpack
    local out = {}
    local totals = 0
    while bytes_read <= max do
        -- print(bytes_read)
        if bytes_read > string.len(s) then break end
        if totals == pop then break end
        local d
        d, bytes_read = struct.unpack(fmt, s, bytes_read)
        d = negation - d
        local zeroes = {}
        while d ~= 0 do
            -- Calculate position of 1
            local d_ones = d
            local inner_zeroes = 0
            while bit.band(d_ones, 1) == 0 do
                inner_zeroes = inner_zeroes + 1
                d_ones = bit.rshift(d_ones, 1)
            end
            -- coroutine.yield(((bytes_read - 1) * 8) - 1 - inner_zeroes)
            -- print(#zeroes + 1)
            zeroes[#zeroes + 1] = ((bytes_read - 1) * 8) - 1 - inner_zeroes
            totals = totals + 1
            d = bit.band(d, d - 1)
        end
        table.sort(zeroes)
        for i, zero in ipairs(zeroes) do coroutine.yield(zero) end
    end

end
