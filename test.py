list1 = [   {'table_catalog': 'dvdrental', 'table_schema': 'public', 'table_name': 'staff'}, 
            {'table_catalog': 'dvdrental', 'table_schema': 'public', 'table_name': 'category'}, 
            {'table_catalog': 'dvdrental', 'table_schema': 'public', 'table_name': 'film_category'}
]

list2 = [   {'table_catalog': 'dvdrental', 'table_schema': 'public', 'table_name': 'staff'}, 
            {'table_catalog': 'dvdrental', 'table_schema': 'public', 'table_name': 'category'}
]

added = []
removed = []

for item in list1:
    if item not in list2:
        removed.append(item)

for item in list2:
    if item not in list1:
        added.append(item)

print("removed")
print(removed)

     

