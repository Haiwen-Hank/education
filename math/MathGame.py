import random
import datetime as dt
import itertools
import re

solution_map = {}
solution_set = {''}


def __solve(num_list, expected_sum=21):
    if len(num_list) != 4:
        return []
    s = ['+', '-', '*', '/']
    sign_high = ['*', '/']
    sign_low = ['+', '-']
    sign_swap = ['+', '*']
    global solution_map
    global solution_set
    a, b, c, d = tuple(num_list)
    h, i, j, k = sorted(num_list)
    set_key = '_'.join([str(expected_sum), str(a), str(b), str(c), str(d)])
    map_key = '_'.join([str(expected_sum), str(h), str(i), str(j), str(k)])
    if set_key in solution_set:
        if map_key in solution_map:
            return solution_map[map_key]
        else:
            return []

    result = []
    solution_set.add(set_key)
    for s1 in s:
        for s2 in s:
            for s3 in s:
                key0 = ''.join([str(a), s1, str(b), s2, str(c), s3, str(d)])
                key1 = ''.join(['(', str(a), s1, str(b), ')', s2, str(c), s3, str(d)])
                key2 = ''.join([str(a), s1, '(', str(b), s2, str(c), ')', s3, str(d)])
                key3 = ''.join([str(a), s1, str(b), s2, '(', str(c), s3, str(d), ')'])
                key5 = ''.join([str(a), s1, '(', str(b), s2, str(c), s3, str(d), ')'])
                key6 = ''.join(['(', str(a), s1, str(b), s2, str(c), ')', s3, str(d)])
                key4 = ''.join(['(', str(a), s1, str(b), ')', s2, '(', str(c), s3, str(d), ')'])

                try:
                    if eval(key0) == expected_sum:
                        result.append(key0)
                except ZeroDivisionError:
                    pass

                if s1 == s2 == s3 and s1 in sign_swap:
                    # key0 can represent all keys
                    continue
                if s1 in sign_low and s2 in sign_high:
                    #
                    try:
                        if eval(key1) == expected_sum:
                            result.append(key1)
                    except ZeroDivisionError:
                        pass

                if s1 in sign_high and s2 in sign_low:
                    #
                    try:
                        if eval(key2) == expected_sum:
                            result.append(key2)
                    except ZeroDivisionError:
                        pass

                if s2 in sign_high and s3 in sign_low:
                    #
                    try:
                        if eval(key3) == expected_sum:
                            result.append(key3)
                    except ZeroDivisionError:
                        pass

                if s2 in sign_high and s3 in sign_low and s1 in sign_low:
                    #
                    try:
                        if eval(key4) == expected_sum:
                            result.append(key4)
                    except ZeroDivisionError:
                        pass

                if s1 in sign_high and (s2 in sign_low or s3 in sign_low):
                    try:
                        if eval(key5) == expected_sum:
                            result.append(key5)
                    except ZeroDivisionError:
                        pass

                if s3 in sign_high and (s2 in sign_low or s1 in sign_low):
                    try:
                        if eval(key6) == expected_sum:
                            result.append(key6)
                    except ZeroDivisionError:
                        pass

    if result is not None and len(result) > 0:
        if map_key in solution_map:
            solution_map[map_key].extend(result)
        else:
            solution_map[map_key] = result
    return result


def find_solution(num_list, expected_sum=21, console=True):
    global solution_map
    global solution_set
    a, b, c, d = tuple(num_list)
    h, i, j, k = sorted(num_list)
    set_key = '_'.join([str(expected_sum), str(a), str(b), str(c), str(d)])
    map_key = '_'.join([str(expected_sum), str(h), str(i), str(j), str(k)])
    if set_key not in solution_set:
        permutation = list(itertools.permutations([a, b, c, d]))
        for num_list in permutation:
            __solve(num_list, expected_sum)
    if map_key in solution_map:
        if console:
            for solution in solution_map[map_key]:
                print(solution)
        return solution_map[map_key]
    else:
        if console:
            print('no solution')
        return []


def cache_solution(start=1, end=11, expct_sum=21):
    start_time = dt.datetime.now()
    for a in range(start, end):
        for b in range(start, end):
            for c in range(start, end):
                for d in range(start, end):
                    find_solution([a, b, c, d], expected_sum=expct_sum, console=False)
    finish_time = dt.datetime.now()
    delta_time = finish_time - start_time
    print('Total seconds used: ', delta_time.seconds)


if __name__ == '__main__':
    score = 0
    while True:
        nums = []
        a = random.randrange(1, 11)
        b = random.randrange(1, 11)
        c = random.randrange(1, 11)
        d = random.randrange(1, 11)
        key = '_'.join([str(i) for i in sorted([a, b, c, d])])
        cached_solution = find_solution([a, b, c, d], expected_sum=21, console=False)
        if cached_solution:
            answer = input(' '.join(['Please enter your answer for ', str(a), str(b), str(c), str(d), ': ']))
        else:
            continue

        answer = answer.replace(' ', '')
        answer_key = '_'.join([str(i) for i in sorted([int(j) for j in re.split("[-*/()\+]", answer) if j])])
        if answer_key != key:
            print('You used wrong numbers')
            break
        elif answer in cached_solution:
            print('You are correct')
            score += 1
        elif eval(answer) == 21:
            print('Your answer is not in my solution list but you are correct')
            score += 1
        else:
            break
    print('Correct answers are: ', cached_solution)
    print('You total score is ', str(score))
