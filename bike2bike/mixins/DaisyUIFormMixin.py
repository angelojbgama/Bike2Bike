from django import forms
from django.utils.safestring import mark_safe

class DaisyUIStyledFormMixin:
    # Define algumas classes padrão
    default_input_class = "input-bordered"
    default_wrapper_class = "input validator items-center"
    default_form_group_class = "form-control gap-1"

    def get_field_styles(self):
        """
        Recupera os estilos definidos em Meta.field_styles no Form.
        """
        return getattr(self.Meta, "field_styles", {})

    def __init__(self, *args, **kwargs):
        """
        No construtor, percorremos todos os campos do formulário,
        definindo classes CSS, placeholders e atributos conforme
        'field_styles' ou conforme a necessidade.
        """
        super().__init__(*args, **kwargs)
        field_styles = self.get_field_styles()

        for field_name, field in self.fields.items():
            style = field_styles.get(field_name, {})
            has_error = self.errors.get(field_name)  # Verifica se esse campo tem erro

            # Define classes padrão do input
            if isinstance(style, dict):
                input_classes = f"{self.default_input_class} {style.get('classes', '')}"
            else:
                input_classes = f"{self.default_input_class} {style}"

            # Se tiver erro, adiciona a classe 'input-error'
            if has_error:
                input_classes += " input-error"

            # Se houver ícones, adiciona 'grow'
            if isinstance(style, dict) and ("icon" in style or "icon_right" in style):
                input_classes += " grow"

            widget = field.widget

            # Ajustes especiais se for Textarea, Select ou FileInput
            if isinstance(widget, forms.Textarea):
                input_classes = f"textarea textarea-bordered {style.get('classes', '')}".strip()
            elif isinstance(widget, forms.Select):
                input_classes = f"select select-bordered {style.get('classes', '')}".strip()
            elif isinstance(widget, forms.ClearableFileInput):
                input_classes = f"file-input file-input-bordered w-full {style.get('classes', '')}".strip()

            # Atribui as classes finais ao widget
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {input_classes}".strip()

            # Define placeholder e demais atributos extras (pattern, title, etc.)
            if isinstance(style, dict):
                widget.attrs.setdefault("placeholder", style.get("placeholder", field.label))
                for attr in ["type", "min", "max", "pattern", "title", "required", "disabled", "list", "autocomplete"]:
                    if attr in style:
                        widget.attrs[attr] = style[attr]
            else:
                widget.attrs.setdefault("placeholder", field.label)

    def render_field(self, name):
        """
        Renderiza cada campo individualmente, incluindo ícones,
        hints e erros. Aqui controlamos a exibição ou não das mensagens.
        """
        field = self.fields[name]
        bf = self[name]  # BoundField (campo + valor + erros)
        style = self.get_field_styles().get(name, {})
        widget = field.widget

        # Variáveis para armazenar HTML extra
        icon_left = ""
        icon_right = ""
        hint_html = ""
        label_html = ""
        suffix_html = ""
        extra_html = ""

        # Verifica se 'style' é dict e obtém ícones, hints, etc.
        if isinstance(style, dict):
            icon_left = style.get("icon", "")
            icon_right = style.get("icon_right", "")
            hint_text = field.help_text or style.get("hint", "")
            
            # Se existir hint, mas queremos que apareça oculto por padrão:
            if hint_text:
                # Adicionamos a classe 'hidden'
                hint_html = f'<div class="validator-hint hidden">{hint_text}</div>'

            suffix_html = style.get("suffix", "")
            extra_html = style.get("extra_html", "")
            
            # Se quisermos exibir o label explicitamente
            if style.get("show_label", False):
                label_html = f'<div class="label"><span class="label-text">{field.label}</span></div>'

        # Cria o bloco de mensagem de erro (oculto por padrão com 'hidden')
        error_html = ""
        if bf.errors:
            error_text = "<br/>".join(str(e) for e in bf.errors)
            # A classe 'text-error' deixa o texto vermelho, 
            # mas 'hidden' garante que ele só aparece se removermos via JS
            error_html = f'<p class="validator-hint hidden text-error">{error_text}</p>'

        # Classes de wrapper para layout
        wrapper_class = style.get("wrapper_class", "w-full")
        row_class = style.get("row_class", "")

        # Layout especial para Checkbox
        if isinstance(widget, forms.CheckboxInput):
            return mark_safe(f"""
                <div class="{row_class}">
                    <div class="{self.default_form_group_class} {wrapper_class}">
                        <label class="label cursor-pointer flex items-center gap-2">
                            {bf} <span class="label-text">{field.label}</span>
                        </label>
                        {hint_html}
                        {error_html}
                        {extra_html}
                    </div>
                </div>
            """)

        # Layout padrão para inputs normais
        return mark_safe(f"""
            <div class="{row_class}">
                <div class="{self.default_form_group_class} {wrapper_class}">
                    {label_html}
                    <label class="{self.default_wrapper_class}">
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
        """
        Retorna todos os campos renderizados, um após o outro.
        """
        return ''.join(self.render_field(name) for name in self.fields)
