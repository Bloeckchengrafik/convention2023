import type { PageLoad } from './$types'
import {endpoint} from "$lib/api";
import type {Pipeline} from "$lib/endpoints";
import {redirect} from "@sveltejs/kit";

export const load = (async ({url}) => {
    const pipeline = await endpoint<Pipeline>('pipeline/new')
    const sourceQuery = url.searchParams.get('source') || 'test'
    throw redirect(301, `/pipelines/prepare/${pipeline.id}/${sourceQuery}`)
}) satisfies PageLoad