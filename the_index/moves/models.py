from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase


class MoveIndexPage(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    content = RichTextField(blank=True)

    indexed_fields = ('title', 'content')

    subpage_types = ['MovePage']

    @property
    def moves(self):
        return MovePage.objects.live().descendant_of(self)

    @property
    def tag_list(self):
        tag_ids = MovePage.objects.all().values_list('tag_id', flat=True)
        return Tag.objects.filter(pk__in=tag_ids)

    def get_context(self, request):
        moves = self.moves

        # tags
        tag = request.GET.get('tag')
        if tag:
            moves = moves.filter(tags__name=tag)

        # pagination
        page = request.GET.get('page')
        paginator = Paginator(moves, 30)
        try:
            moves = paginator.page(page)
        except PageNotAnInteger:
            moves = paginator.page(1)
        except EmptyPage:
            moves = paginator.page(paginator.num_pages)

        # update context
        context = super(MoveIndexPage, self).get_context(request)
        context['moves'] = moves
        return context

MoveIndexPage.content_panels =[
    FieldPanel('title', classname="full title"),
    FieldPanel('content'),
]

class MovePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'moves.MovePage', related_name='tagged_items'
    )

class MovePage(Page):
    description = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=MovePageTag, blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('info', 'description', 'content', 'tags')

MovePage.content_panels = Page.content_panels + [
    StreamFieldPanel('info'),
    FieldPanel('description'),
    FieldPanel('content'),
    ImageChooserPanel('image'),
    FieldPanel('tags'),
    InlinePanel('credits', label="Credits")
]


