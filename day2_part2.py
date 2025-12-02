# Advent of Code - Day 2 Part 2

ranges = "4077-5314,527473787-527596071,709-872,2487-3128,6522872-6618473,69137-81535,7276-8396,93812865-93928569,283900-352379,72-83,7373727756-7373754121,41389868-41438993,5757-6921,85-102,2-16,205918-243465,842786811-842935210,578553879-578609405,9881643-10095708,771165-985774,592441-692926,7427694-7538897,977-1245,44435414-44469747,74184149-74342346,433590-529427,19061209-19292668,531980-562808,34094-40289,4148369957-4148478173,67705780-67877150,20-42,8501-10229,1423280262-1423531012,1926-2452,85940-109708,293-351,53-71"


def is_invalid(n):
    s = str(n)
    length = len(s)

    # Try all possible repeating unit lengths
    for size in range(1, length // 2 + 1):
        if length % size == 0:
            unit = s[:size]
            if unit * (length // size) == s:
                return True

    return False


total_sum = 0

for part in ranges.split(","):
    start, end = map(int, part.split("-"))

    for number in range(start, end + 1):
        if is_invalid(number):
            total_sum += number

print("Day 2 Part 2 Answer:", total_sum)
