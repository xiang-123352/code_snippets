#include <gladeui/glade.h>

static void
transfer_properties (GObject *object,
                     GladeWidget *gwidget,
                     GladeWidget *gchild,
                     GObject *child,
                     const GList *props)
{
  const GList *l;

  for (l = props; l; l = g_list_next (l))
    {
      GladeProperty *prop = l->data;
      GladePropertyClass *pclass = glade_property_get_class (prop);
      GParamSpec *pspec = glade_property_class_get_pspec (pclass);
      GValue value = {0, };
      const gchar *id;

      if (glade_property_class_get_virtual (pclass) ||
          glade_property_class_get_construct_only (pclass) ||
          !(pspec->flags & G_PARAM_READABLE) ||
          !(pspec->flags & G_PARAM_WRITABLE))
        continue;

      g_value_init (&value, G_PARAM_SPEC_VALUE_TYPE (pspec));

      id = glade_property_class_id (pclass);

      if (gchild)
        gtk_container_child_get_property (GTK_CONTAINER (object),
                                          GTK_WIDGET (child),
                                          id, &value);
      else
        g_object_get_property (object, id, &value);

      glade_property_set_value (prop, &value);

      g_value_unset (&value);
    }
}

static GladeWidget *
glade_project_add_widget_from_object (GladeProject *project, GObject *object, GladeWidget *widget)
{
  GladeWidgetAdaptor *adaptor = glade_widget_adaptor_get_by_type (G_OBJECT_TYPE (object));

  if (adaptor == NULL)
    {
      g_warning ("Widget type %s is not supported by glade", G_OBJECT_TYPE_NAME (object));
      return NULL;
    }

  if (!widget)
    {
      widget = glade_widget_adaptor_create_widget (adaptor, FALSE,
                                                   "project", project,
                                                   "reason", GLADE_CREATE_LOAD,
                                                   NULL);

      glade_project_add_object (project, glade_widget_get_object (widget));
    }

  /* Transfer properties */
  transfer_properties (object, widget, NULL, NULL, 
                       glade_widget_get_properties (widget));

  if (GTK_IS_CONTAINER (object))
    {
      GList *l, *children = gtk_container_get_children (GTK_CONTAINER (object));

      for (l = children; l; l = g_list_next (l))
        {
          GladeWidget *gchild = NULL;
          gchar *internal_name;

          if ((internal_name = g_object_get_data (l->data, "glade-dump-internal-name")))
            {
              GtkWidget *parent = GTK_WIDGET (glade_widget_get_object (widget));
              GObject *obj;

              while (parent)
                {
                  obj = glade_widget_adaptor_get_internal_child (glade_widget_adaptor_get_by_type (G_OBJECT_TYPE (parent)),
                                                                 G_OBJECT (parent),
                                                                 internal_name);

                  if (obj)
                    break;

                  parent = gtk_widget_get_parent (parent);
                }

              if (obj == NULL)
                continue;

              gchild = glade_widget_get_from_gobject (obj);
              glade_project_add_widget_from_object (project, l->data, gchild);
            }
          else
            {
              gchild = glade_project_add_widget_from_object (project, l->data, NULL);
              glade_widget_set_parent (gchild, widget);
              glade_widget_adaptor_add (adaptor, glade_widget_get_object (widget),
                                        glade_widget_get_object (gchild));
            }

          if (gchild)
            /* Transfer packing properties */
            transfer_properties (object, glade_widget_get_parent (gchild), gchild, l->data,
                                 glade_widget_get_packing_properties (gchild));
        }

      g_list_free (children);
    }
  return widget;
}

#define INTERNAL_CHILD(obj,name) g_object_set_data (G_OBJECT(obj), "glade-dump-internal-name", name)

static void
dump_widget (GtkWidget *widget, const gchar *path)
{
  /* Create a Glade project */
  GladeProject *project = glade_project_new ();

  /* add as many widget you want in the project */
  glade_project_add_widget_from_object (project, G_OBJECT (widget), NULL);

  /* And save it to a file */
  glade_project_save (project, path, NULL);

  /* And do not forget to free memory (I know it is pointless since this code will be removed anyways ) */
  g_object_unref (project);
}

