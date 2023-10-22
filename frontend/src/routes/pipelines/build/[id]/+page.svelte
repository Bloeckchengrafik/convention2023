<script lang="ts">
    import type {PageData} from "./$types";
    import {endpoint, root} from "$lib/api";
    import {goto} from "$app/navigation";

    export let data: PageData;
</script>

<div class="h-full row">
    <div class="column d-flex flex-column">
        <div class="steps">
            <span class="step-item">
                Pipeline creation
            </span>
            <span class="step-item">
                Sample capturing
            </span>
            <span class="step-item">
                Sample processing
            </span>
            <span class="step-item active">
                Model building
            </span>
            <span class="step-item">
                Cutting
            </span>
        </div>
        <div class="card mt-4 flex-grow-1">
            <div class="card-header">
                <div class="card-title">
                    <h1>Building Model for #{data.id}</h1>
                </div>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center flex-column gap-3 p-5">
                <img src="{root}pipeline/current_preview_image" alt="PREVIEW" style="height: 400px">
                <div class="d-flex gap-3">
                    <button class="btn btn-primary" on:click={async () => {
                        await endpoint("pipeline/id/" + data.id + "/slice")
                        await new Promise(resolve => setTimeout(resolve, 500))
                        await endpoint("pipeline/id/" + data.id + "/cut")
                        await goto("/pipelines/cutting/" + data.id )
                    }}>
                        Build Model
                    </button>
                    <button class="btn btn-primary" on:click={async () => {
                        await endpoint("pipeline/id/" + data.id + "/cancel")
                        await goto("/")
                    }}>
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>