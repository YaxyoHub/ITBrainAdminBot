start => 

Menu (Default Keyboard) \|/

  Davomat    |  Sinflar  
O'quvchilar  | O'qituvchilar
Kirim-Chiqim | 

1) Davomat -> bosilsa,

menu->
Kelgan o'quvchini belgilash | Kelmagan o'quvchilarni ko'rish
                   Asosiy menuga qaytish

Kelgan o'quvchini belgilash -> 
O'quvchi ism-familyasi kiritiladi

Kelmagan o'quvchilarni ko'rish -> 
Belgilanmagan o'quvchilar ism-familyasi chiqadi

Asosiy menuga qaytish -> 
Menuga qaytish

2) Sinflar -> bosilsa,

menu->
   Sinf qo'shish  |  Sinf o'chirish
Sinflarni ko'rish | Asosiy menuga qaytish

Sinf qo'shish -> 
statelar bilan yangi Sinf qo'shish

Sinf o'chirish ->
Sinfni o'chirish

Sinflarni ko'rish ->
Default menuda sinflar chiqadi
menu->
Sinf A  |  Sinf B  | Sinf C
Sinf D  |  Sinf E  | Sinf H
  Sinflar menusiga qaytish

Asosiy menuga qaytish ->
Asosiy menuga qaytish

3) O'quvchilar -> bosilsa,

menu->
   O'quvchi qo'shish  |  O'quvchi o'chirish
O'quvchilani ko'rish  | Asosiy menuga qaytish

O'quvchi qo'shish -> 
state'lar bilan yangi o'quvchi qo'shish
 \|/
Ism-familya,
Telefon raqam,
Course turi (Backend, Frontent, Ingliz tili),
Sinf (7A, 8B)


O'quvchilani ko'rish ->
O'quvchilar ro'yxatini ko'rish

message ->
O'quv markazda n ta o'quvchi bor.
Ular haqida ko'proq ma'lumot bilish uchun 
sinf orqali ularni toping va ma'lumot oling

Asosiy menuga qaytish -> 
Asosiy menuga qaytish

4) O'qituvchilar -> bosilsa,

menu->
   O'qituvchi qo'shish  |  O'qituvchi o'chirish
O'qituvchilani ko'rish  | Asosiy menuga qaytish

O'qituvchi qo'shish -> 
state'lar bilan yangi o'qituvchi qo'shish
 \|/
Ism-familya,
Telefon raqam,
Telegram nickname
Yunalishi (Backend, Frontent, Ingliz tili),

O'qituvchi o'chirish -> 
o'quvchi o'chirish 


O'qituvchilani ko'rish ->
O'quvchilar ro'yxatini ko'rish

Asosiy menuga qaytish -> 
Asosiy menuga qaytish

O'quvchilar ->

Ism-familya TEXT,
Telefon raqam TEXT,
Course turi (Backend, Frontent, Ingliz tili) TEXT,,
Sinf (7A, 8B) TEXT,
Aktiv null True False

O'qituvchi ->

Ism-familya TEXT,
Telefon raqam TEXT,
Telegram nickname TEXT,
Yunalishi (Backend, Frontent, Ingliz tili) TEXT,
Sinflar (7A, 8B) TEXT[]

Sinflar -> 

Nomi 7A, 8B TEXT,
Yunalish Backend, Frontent TEXT,
O'qituvchisi TEXT,
Vaqti 10:00-12:00 TEXT,
O'quvchilar_soni INTEGER,
O'quvchilar TEXT

To'lovlar -> bosilsa,

sinflar chiqadi  
7A | 8B | 9K
6H | 5R | 4F

sinf tanlansa usha sinf oquvchilari chiqadi
1. Yaxyo | 250 000 (agar tulob qilgan bulsa)
2. Avazbek
3. Aziz
4. ...

Va id soraladi
usha idli odam uchun tolob summasi kiritiladi
va message uzgaradi

