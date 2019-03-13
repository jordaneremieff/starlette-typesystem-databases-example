import typesystem


class UserSchema(typesystem.Schema):
    id = typesystem.Integer(allow_null=True)
    name = typesystem.String(max_length=100)

    def __str__(self) -> str:
        return f"#{self.id} - {self.name}"
