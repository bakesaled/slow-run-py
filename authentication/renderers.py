from core.renderers import ConduitJSONRenderer


class UserJSONRenderer(ConduitJSONRenderer):
  object_label = 'user'

  def render(self, data, media_type=None, renderer_context=None):
    errors = data.get('errors', None)

    return super(UserJSONRenderer, self).render(data)
