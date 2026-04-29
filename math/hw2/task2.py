import itertools

def check_access(is_employee, is_verified, is_premium, is_admin, is_banned):
    base = is_employee and is_verified and not is_banned
    premium = (is_employee or is_premium) and is_verified and not is_banned
    admin = is_admin and is_verified and not is_banned
    secret = (is_admin or (is_employee and is_premium)) and is_verified and not is_banned
    return {'Base': base, 'Premium': premium, 'Admin': admin, 'Secret': secret}

# Заголовок таблиці
print("Emp Ver Prem Adm Ban | Base Prem Admin Secret")
print("-" * 50)

full_access_count = 0
premium_no_base = []

for combo in itertools.product([True, False], repeat=5):
    emp, ver, prem, adm, ban = combo
    result = check_access(emp, ver, prem, adm, ban)
    base_int = int(result['Base'])
    prem_int = int(result['Premium'])
    adm_int = int(result['Admin'])
    secr_int = int(result['Secret'])

    print(f"{int(emp)}   {int(ver)}   {int(prem)}    {int(adm)}   {int(ban)}  |  "
          f"{base_int}    {prem_int}    {adm_int}     {secr_int}")

    if all([base_int, prem_int, adm_int, secr_int]):
        full_access_count += 1
    if prem_int == 1 and base_int == 0:
        premium_no_base.append(combo)

print(f"\nКількість комбінацій з повним доступом до усіх 4 секцій: {full_access_count}")

if premium_no_base:
    print("\nКомбінації з доступом до Premium, але не до Base:")
    for c in premium_no_base:
        print(c)
    print("\nПояснення: Таке можливо, бо Premium дається, якщо користувач співробітник або має Premium-підписку, "
          "а Base — тільки якщо співробітник. Тобто користувач з преміумом, але не співробітник, має Premium, але не Base.")
else:
    print("\nКомбінацій з доступом до Premium, але без доступу до Base немає.")


"""
Відповіді на питання:

Скільки випадків з повним доступом — виводить змінна full_access_count.

Чи є випадки з доступом до Premium, але не до Base — якщо так, виводить їх і пояснює, що це користувачі, які мають преміум, але не є співробітниками, тому Base не мають.
"""
