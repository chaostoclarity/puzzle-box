// Pixel art on a 3D surface.
// Crisp texels (nearest filter, no mipmaps) and lighting snapped to 4 steps,
// so faces turning away from the camera darken in clean bands instead of smooth gradients.
shader_type spatial;
render_mode unshaded, cull_disabled;

uniform sampler2D tex : source_color, filter_nearest;
uniform float highlight = 0.0;
uniform float back_shade = 0.35;

void fragment() {
	vec4 c = texture(tex, UV);
	float facing = FRONT_FACING ? max(dot(NORMAL, vec3(0.0, 0.0, 1.0)), 0.0) : 0.0;
	float light = FRONT_FACING ? mix(0.45, 1.0, facing) : back_shade;
	light = floor(light * 4.0 + 0.5) / 4.0;
	ALBEDO = c.rgb * light + vec3(highlight);
	ALPHA = c.a;
	ALPHA_SCISSOR_THRESHOLD = 0.5;
}
