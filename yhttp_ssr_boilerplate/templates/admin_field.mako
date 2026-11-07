<%page args="field, form_id" />
<div class="min-w-0 ${'md:col-span-2' if field['type'] == 'textarea' else ''}">
  <label class="mb-2 block text-sm font-medium" for="${form_id | h}">${field['label'] | h}</label>
  % if field['type'] == 'textarea':
    <textarea class="min-h-28 w-full border border-color-2/45 bg-color-5 px-4 py-3 text-sm leading-6 text-color-4 outline-none focus:border-color-4" id="${form_id | h}" name="${field['name'] | h}" maxlength="${field['maxlength']}" required>${field['value'] | h}</textarea>
  % elif field['type'] == 'select':
    <select class="min-h-11 w-full border border-color-2/45 bg-color-5 px-3 py-2 text-sm text-color-4 outline-none focus:border-color-4" id="${form_id | h}" name="${field['name'] | h}">
      % for option in field['options']:
        <option value="${option['value'] | h}" ${'selected' if option['value'] == field['value'] else ''}>${option['label'] | h}</option>
      % endfor
    </select>
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
    <input class="min-h-11 w-full border border-color-2/45 bg-color-5 px-4 py-2.5 text-sm text-color-4 outline-none focus:border-color-4" type="text" id="${form_id | h}" name="${field['name'] | h}" value="${field['value'] | h}" maxlength="${field['maxlength']}" required>
  % endif
  % if field['name'] in ('headline', 'primary_cta_href', 'secondary_cta_href'):
    <p class="mt-1 text-xs leading-5 text-color-2">Use plain text. Destinations accept a homepage section anchor, a site path, or an HTTPS URL.</p>
  % elif field['name'] == 'additional_asset_ids':
    <p class="mt-1 text-xs leading-5 text-color-2">Choose extra images for this project. Alt text for each placement can be added in the media library.</p>
  % elif field['name'] == 'availability':
    <p class="mt-1 text-xs leading-5 text-color-2">Available resources require a valid file or HTTPS resource URL.</p>
  % elif field['name'] == 'cover_alt':
    <p class="mt-1 text-xs leading-5 text-color-2">Leave blank to use the media asset’s default alt text. Mark the image decorative when it adds no information.</p>
  % endif
</div>
