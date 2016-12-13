function(N)
    for i=0,N do
        coroutine.yield( i%2 )
    end
end
