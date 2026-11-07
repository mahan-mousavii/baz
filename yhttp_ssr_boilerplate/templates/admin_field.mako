<%page args="field, form_id, csrf" />
<div class="min-w-0 ${'md:col-span-2' if field['type'] == 'textarea' else ''}">
  <label id="${form_id | h}-label" class="mb-2 block text-sm font-semibold" for="${form_id | h}">${field['label'] | h}<span class="ml-2 text-xs font-normal text-color-2">${'Required' if field['required'] else 'Optional'}</span></label>
  % if field['type'] == 'textarea':
    <textarea class="min-h-28 w-full border border-color-2/45 bg-color-5 px-4 py-3 text-sm leading-6 text-color-4 outline-none focus:border-color-4" id="${form_id | h}" name="${field['name'] | h}" maxlength="${field['maxlength']}" aria-describedby="${form_id | h}-help ${form_id | h}-error" ${'aria-invalid="true"' if field.get('error') else ''} ${'required' if field['required'] else ''}>${field['value'] | h}</textarea>
  % elif field['type'] == 'select':
    <select class="min-h-11 w-full border border-color-2/45 bg-color-5 px-3 py-2 text-sm text-color-4 outline-none focus:border-color-4" id="${form_id | h}" name="${field['name'] | h}" aria-describedby="${form_id | h}-help ${form_id | h}-error" ${'aria-invalid="true"' if field.get('error') else ''} ${'required' if field['required'] else ''}>
      % for option in field['options']:
        <option value="${option['value'] | h}" ${'selected' if option['value'] == field['value'] else ''}>${option['label'] | h}</option>
      % endfor
    </select>
  % elif field['type'] == 'image_asset':
    <% selected = field.get('selected_asset') %>
    <div class="space-y-3" role="group" aria-labelledby="${form_id | h}-label" x-data="cmsImageField" x-init="init($el)" data-csrf="${csrf | h}" data-field-id="${form_id | h}" data-current-filename="${(selected['filename'] if selected else '') | h}" data-current-preview="${(selected['preview_url'] if selected else '') | h}" aria-describedby="${form_id | h}-help ${form_id | h}-error">
      <input type="hidden" id="${form_id | h}" name="${field['name'] | h}" value="${field['value'] | h}" x-ref="value">
      <div class="flex flex-col gap-4 border border-color-2/30 bg-color-1/50 p-4 sm:flex-row sm:items-center">
        <div class="flex size-28 shrink-0 items-center justify-center overflow-hidden border border-color-2/25 bg-color-5" aria-live="polite">
          <img x-show="previewUrl" :src="previewUrl" :alt="filename ? 'Current image: ' + filename : ''" class="h-full w-full object-cover" x-cloak>
          <span x-show="!previewUrl" class="px-3 text-center text-xs leading-5 text-color-2">No image selected</span>
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-semibold uppercase tracking-wider text-color-2">Current image</p>
          <p class="mt-1 break-all text-sm font-medium" x-text="filename || 'Optional image slot'"></p>
          <p class="mt-1 text-xs leading-5 text-color-2">Choose a library image or upload one. Changes take effect after you save or publish.</p>
          <div class="mt-3 flex flex-wrap gap-2">
            <button type="button" class="min-h-10 bg-color-4 px-3 py-2 text-xs font-medium text-color-5 hover:bg-color-4/90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-color-4" @click="openPicker($el)">Choose from Media Library</button>
            <label class="min-h-10 cursor-pointer border border-color-4/35 px-3 py-2 text-xs hover:bg-color-4/10 focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-color-4">
              <span x-text="uploading ? 'Uploading…' : 'Upload new image'"></span>
              <input class="sr-only" type="file" accept=".jpg,.jpeg,.png,.webp" :disabled="uploading" @change="upload($event)">
            </label>
            <button type="button" class="min-h-10 border border-color-4/25 px-3 py-2 text-xs text-color-2 hover:border-color-4/50 hover:text-color-4" :disabled="!$refs.value.value" @click="clear()">Remove from this section</button>
          </div>
          <p class="mt-2 text-xs text-color-2" role="status" aria-live="polite" x-text="message"></p>
        </div>
      </div>
      <dialog class="w-[min(56rem,calc(100%-2rem))] max-h-[85vh] max-w-none overflow-y-auto border border-color-4/25 bg-color-5 p-0 text-color-4 shadow-2xl backdrop:bg-color-4/60" aria-labelledby="${form_id | h}-picker-title" @close="onClose()" x-ref="dialog">
        <div class="sticky top-0 z-10 border-b border-color-4/20 bg-color-5 p-4 sm:p-6">
          <div class="flex items-start justify-between gap-4">
            <div><h2 id="${form_id | h}-picker-title" class="text-xl font-semibold">Choose an image</h2><p class="mt-1 text-sm text-color-2">Select an image, then confirm to update this field.</p></div>
            <button type="button" class="min-h-10 border border-color-4/25 px-3 text-sm focus-visible:outline-2 focus-visible:outline-color-4" @click="cancel()">Cancel</button>
          </div>
          <label class="mt-4 block text-sm font-medium" :for="'search-' + $id('picker-search')">Search filenames</label>
          <input class="mt-1 min-h-11 w-full border border-color-2/45 bg-white px-3 text-sm outline-none focus:border-color-4" :id="'search-' + $id('picker-search')" type="search" x-model="search" @input.debounce.250ms="load(1)" placeholder="Search by filename">
        </div>
        <div class="p-4 sm:p-6">
          <p class="mb-4 text-sm text-color-2" role="status" aria-live="polite" x-text="pickerMessage"></p>
          <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            <template x-for="item in items" :key="item.id">
              <button type="button" class="min-w-0 border p-2 text-left focus-visible:outline-2 focus-visible:outline-color-4" :class="candidate?.id === item.id ? 'border-color-3 bg-color-3/10 ring-2 ring-color-3' : 'border-color-2/30 hover:border-color-4/60'" :aria-pressed="candidate?.id === item.id" @click="candidate = item">
                <img class="aspect-[4/3] w-full bg-white object-cover" :src="item.preview_url" :alt="'Preview of ' + item.filename" loading="lazy">
                <span class="mt-2 block break-all text-xs font-medium" x-text="item.filename"></span>
                <span class="mt-1 block text-[0.7rem] text-color-2" x-text="metadata(item)"></span>
              </button>
            </template>
          </div>
          <div class="mt-4 flex flex-wrap items-center justify-between gap-3">
            <button type="button" class="min-h-10 border border-color-4/25 px-3 text-sm disabled:opacity-50" x-show="hasMore" :disabled="loading" @click="load(page + 1, true)">Load more</button>
            <div class="ml-auto flex gap-2">
              <button type="button" class="min-h-10 border border-color-4/25 px-4 text-sm" @click="cancel()">Cancel</button>
              <button type="button" class="min-h-10 bg-color-4 px-4 text-sm font-medium text-color-5 disabled:opacity-50" :disabled="!candidate" @click="select()">Select image</button>
            </div>
          </div>
        </div>
      </dialog>
    </div>
  % elif field['type'] == 'multi_image_asset':
    % if field['options']:
      <div class="max-h-48 space-y-2 overflow-y-auto border border-color-2/35 bg-color-5 p-3">
        % for option in field['options']:
          <label class="flex min-h-10 items-center gap-3 text-sm">
            <input class="size-4 accent-color-4" type="checkbox" name="${field['name'] | h}" value="${option['value'] | h}" ${'checked' if option['selected'] else ''}>
            <span class="break-all">${option['label'] | h}</span>
          </label>
        % endfor
      </div>
    % else:
      <p class="border border-color-2/35 bg-color-5 px-3 py-3 text-sm text-color-2">Upload images in the media library first.</p>
    % endif
  % elif field['type'] == 'checkbox':
    <label class="flex min-h-11 items-center gap-3 border border-color-2/35 bg-color-5 px-3 py-2 text-sm">
      <input class="size-4 accent-color-4" type="checkbox" id="${form_id | h}" name="${field['name'] | h}" value="yes" ${'checked' if field['value'] else ''}>
      ${field['label'] | h}
    </label>
  % else:
    <input class="min-h-11 w-full border border-color-2/45 bg-color-5 px-4 py-2.5 text-sm text-color-4 outline-none focus:border-color-4" type="text" id="${form_id | h}" name="${field['name'] | h}" value="${field['value'] | h}" maxlength="${field['maxlength']}" aria-describedby="${form_id | h}-help ${form_id | h}-error" ${'aria-invalid="true"' if field.get('error') else ''} ${'required' if field['required'] else ''}>
  % endif
  % if field.get('error'):
    <p id="${form_id | h}-error" class="mt-1 text-sm font-medium text-red-300" role="alert">${field['error'] | h}</p>
  % endif
  % if field['type'] not in ('checkbox', 'multi_image_asset'):
    <p id="${form_id | h}-help" class="mt-1 text-xs leading-5 text-color-2">Maximum ${field['maxlength']} characters. ${'Use plain text. Destinations accept a homepage section anchor, a site path, or an HTTPS URL.' if field['name'] in ('primary_cta_href', 'secondary_cta_href') else ''}</p>
  % endif
  % if field['name'] in ('headline', 'primary_cta_href', 'secondary_cta_href'):
    % if field['name'] == 'headline':
      <p class="mt-1 text-xs leading-5 text-color-2">Use a line break to control the two-line headline.</p>
    % endif
  % elif field['name'] == 'additional_asset_ids':
    <p class="mt-1 text-xs leading-5 text-color-2">Choose extra images for this project. Alt text for each placement can be added in the media library.</p>
  % elif field['name'] == 'availability':
    <p class="mt-1 text-xs leading-5 text-color-2">Available resources require a valid file or HTTPS resource URL.</p>
  % elif field['name'] == 'cover_alt':
    <p class="mt-1 text-xs leading-5 text-color-2">Leave blank to use the media asset’s default alt text. Mark the image decorative when it adds no information.</p>
  % endif
</div>
