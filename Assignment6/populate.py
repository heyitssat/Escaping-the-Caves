import numpy as np
import random
import utilities

block_size = utilities.DIM_X * utilities.DIM_Y * utilities.DIM_Z
msg_size = block_size - 16

flags = [0]*(1<<16)
cnt = 0

def get_block_digest(msg):
    assert len(msg) == block_size
    np_msg = np.array(msg)
    np_msg.resize(utilities.DIM_X, utilities.DIM_Y, utilities.DIM_Z)
    np_msg[3:,4,:] = 0

    np_digest = utilities.weccakf(np_msg)
    np_digest.resize(np_digest.size)

    digest_suffix = np_digest[msg_size:]
    ind = 0
    for i in digest_suffix:
        ind = (ind<<1)|i
    if not flags[ind]:
        global cnt
        cnt += 1
        flags[ind] = 1

random.seed()

prev_cnt = cnt
cnt_lim = len(flags)
loop_count = 0

print('# loops\t# hits')
while cnt < cnt_lim:
    try:
        msg = [random.randint(0,1) for i in range(block_size)]
        get_block_digest(msg)

        loop_count += 1

        if not (cnt&(cnt-1)):
            if cnt != prev_cnt:
                print('{}\t{}'.format(loop_count, cnt))
                prev_cnt = cnt
        elif not loop_count&(loop_count-1):
            print('{}\t{}'.format(loop_count, cnt))
            prev_cnt = cnt

    except KeyboardInterrupt:
        print(loop_count, cnt)
