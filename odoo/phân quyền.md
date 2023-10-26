# Phân quyền Odoo

---

## Tổng quan

3 loại phân quyền: 

1. Access Rights: phân quyền CRUD group user - model.
2. Theo Field: xác định những group user được phép access field của model. 
3. Theo record: ví dụ: nếu có 'points != null' thì không được xóa row này. 

Nguồn odoo: 
- https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started/05_securityintro.html
- https://www.odoo.com/documentation/16.0/developer/tutorials/restrict_data_access.html

Cách phân quyền trong odoo: tạo category > tạo groups > phân quyền dựa trên các groups này.


---

## Ví dụ

Để dễ hiểu: 

Sau đây sẽ là 1 cách có thể dùng để phân quyền cho funix. Ý tưởng: 
- Tạo module `funix-user` chứa category và groups
- Các modules khác sẽ sử dụng groups của module `funix-user` để phân quyền. 


#### 1. Tạo module `funix-user`

```shell
(env) ./odoo-bin scaffold <module name> <addons direactory>
# vd
(env) ./odoo-bin scaffold funix-user /home/$USER/workspace/Portal/portal-addons
```

#### 2. Tạo category và groups

Tạo Category Funix có 2 groups: admin, mentor:
- admin có thể CRUD. 
- mentor chỉ có thể R.

File `security/security.xml`: 

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- TẠO CATEGORY  -->
    <!-- id tùy ý nhưng phải là duy nhất trong module -->
    <record id="module_category_funix" model="ir.module.category">
        <field name="name">Funix</field> <!-- tên của Category -->
        <field name="description">Nhân viên Funix.</field> <!-- mô tả Category -->
    </record>

    <!-- TẠO GROUP FUNIX MENTOR -->
    <record id="group_funix_user_mentor" model="res.groups">
        <field name="name">Funix Mentor</field>
        <field name="category_id" ref="module_category_funix"/>  <!-- id của category trên -->
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>   <!-- base.group_user là group có sẵn của odoo. '4' là gì thì đọc chú thích ở cuối bài -->
        <field name="comment">Funix Mentor</field> <!-- Mô tả -->
    </record>

    <!-- TẠO GROUP FUNIX ADMIN là kế thừa FUNIX MENTOR -->
    <record id="group_funix_user_admin" model="res.groups">
        <field name="name">Funix Admin</field>
        <field name="category_id" ref="module_category_funix"/>  
        <field name="implied_ids" eval="[(4, ref('group_funix_user_mentor'))]"/> 
        <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/> <!-- base.user_root và base.user_admin có quyền như admin -->
        <field name="comment">Funix Admin</field>
    </record>
</odoo>
```

#### 3. Ở module muốn phân quyền (vd: `assignment`), set Acces Right (CRUD):
- `__manifest__.py`: thêm funix-user vào depends, trước module cần dùng

```python
{
    'depends': ['base', 'funix-user', 'assignment',...],
}
```

- File `security/ir.model.access.csv`:

```csv
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_<tên model>,access_<tên model>,model_<tên model>,<group>,1,0,0,0

VD set CRUD cho assignment_course
admin_assignment_course,admin_assignment_course,model_assignment_course,funix-user.group_funix_user_admin,1,1,1,1 ===> admin
mentor_assignment_course,mentor_assignment_course,model_assignment_course,funix-user.group_funix_user_mentor,1,0,0,0 ===> mentor
```

### 4. Set rule cho record nếu cần. VD: không cho phép các user không phải là author sửa, xóa assignment_course:

Tại module assignment, file `security/security.xml`: 

```xml
<odoo>
    <record id="test_rule" model="ir.rule">
        <field name="name">Test rule</field>
        <field name="model_id" ref="assignment.model_assignment_course"/>
        <field name="domain_force">[('create_uid', '=', user.id)]</field>  
        <field name="perm_read" eval="False" />
        <field name="perm_write" eval="True" />
        <field name="perm_unlink" eval="True" />
        <field name="perm_create" eval="False" />
    </record>
</odoo>
```

Ngoài ra: 
- Thêm `groups=...` vào field ở views để restrict access vị trí tương ứng (view tree, form). 
- Thêm `groups=...` vào field khi tạo model để restrict access mọi nơi. 

**API:** mình chưa tìm hiểu kỹ về external api. Đọc qua thì sẽ sử dụng thư viện của odoo, kết nối với odoo qua username và password hoặc token của user đó > không cần làm gì thêm. 

---

### Note (nguồn google)

1. `users` are the group members which will get all the group privileges. The model behind is res.users. Example: Users in the group sales manager will see the sales configuration menu.

2. `implied_ids` are inherited group privileges. A group which inherits other groups, will get all the other groups rights in top of their own. The model behind is res.groups. Example: The group sales manager will inherit all rights from group see all leads which also implies the rights from group see own leads.

3. `4` is one of the relational field write operations. It literally means "add (4) the following ID to the relation". The following ID in this example is produced/got by the ref function, which gets a external ID or XML ID and replaces that by an actual database ID. Other write operations are 3 or 6 (or many2many fields), which look like [(3, ID)] and [(6, 0, List_of_IDs)]. They read like "remove (3) the relation to ID, but dont delete the row of ID" (look into 2, it would delete it) and "replace all relations (6) with new relations to List_of_IDs". 
