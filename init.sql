
CREATE TABLE IF NOT EXISTS public.task1
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    label text COLLATE pg_catalog."default",
    data jsonb,
    created timestamp without time zone DEFAULT now(),
    updated timestamp without time zone DEFAULT now(),
    CONSTRAINT task1_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.task1
    OWNER to postgres;