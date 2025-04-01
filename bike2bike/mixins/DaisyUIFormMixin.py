from django import forms
from django.utils.safestring import mark_safe

class DaisyUIStyledFormMixin:
    """
    Mixin sem classes padrão fixas. Tudo é controlado via field_styles.
    Quando houver ícones, são aplicadas classes específicas dinamicamente.
    """

    def get_field_styles(self):
        return getattr(self.Meta, "field_styles", {})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_styles = self.get_field_styles()

        for field_name, field in self.fields.items():
            style = field_styles.get(field_name, {})
            has_error = self.errors.get(field_name)
            widget = field.widget

            # Classes base do input
            if isinstance(style, dict):
                input_classes = style.get("classes", "")
            else:
                input_classes = style

            # Adiciona classe de erro
            if has_error:
                input_classes += " input-error"

            # Aplica `grow` se houver ícones
            if isinstance(style, dict) and ("icon" in style or "icon_right" in style):
                input_classes += " grow"

            # Atribui classes finais ao widget
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {input_classes}".strip()

            # Aplica atributos extras definidos no style
            if isinstance(style, dict):
                widget.attrs.setdefault("placeholder", style.get("placeholder", field.label))
                for attr in ["type", "min", "max", "pattern", "title", "required", "disabled", "list", "autocomplete"]:
                    if attr in style:
                        widget.attrs[attr] = style[attr]
            else:
                widget.attrs.setdefault("placeholder", field.label)

    def render_field(self, name):
        field = self.fields[name]
        bf = self[name]
        style = self.get_field_styles().get(name, {})
        widget = field.widget

        icon_left = ""
        icon_right = ""
        hint_html = ""
        label_html = ""
        suffix_html = ""
        extra_html = ""

        if isinstance(style, dict):
            icon_left = style.get("icon", "")
            icon_right = style.get("icon_right", "")
            hint_text = field.help_text or style.get("hint", "")
            if hint_text:
                hint_html = f'<div class="validator-hint hidden">{hint_text}</div>'

            suffix_html = style.get("suffix", "")
            extra_html = style.get("extra_html", "")
            if style.get("show_label", False):
                label_html = f'<div class="label"><span class="label-text">{field.label}</span></div>'

        error_html = ""
        if bf.errors:
            error_text = "<br/>".join(str(e) for e in bf.errors)
            error_html = f'<p class="validator-hint hidden text-error">{error_text}</p>'

        wrapper_class = style.get("wrapper_class", "w-full")
        row_class = style.get("row_class", "")

        # Aplica wrapper especial com ícone, se necessário
        icon_wrapper_class = "input validator items-center" if icon_left or icon_right else ""

        # Layout para checkbox
        if isinstance(widget, forms.CheckboxInput):
            return mark_safe(f"""
                <div class="{row_class}">
                    <div class="{wrapper_class}">
                        <label class="label cursor-pointer flex items-center gap-2">
                            {bf} <span class="label-text">{field.label}</span>
                        </label>
                        {hint_html}
                        {error_html}
                        {extra_html}
                    </div>
                </div>
            """)

        # Layout padrão com suporte a ícones
        return mark_safe(f"""
            <div class="{row_class}">
                <div class="{wrapper_class}">
                    {label_html}
                    <label class="{icon_wrapper_class}">
                        {icon_left}
                        {bf}
                        {icon_right}
                        {suffix_html}
                    </label>
                    {hint_html}
                    {error_html}
                    {extra_html}
                </div>
            </div>
        """)

    def as_div(self):
        return ''.join(self.render_field(name) for name in self.fields)
