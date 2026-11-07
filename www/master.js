import Alpine from 'alpinejs';

window.Alpine = Alpine;
Alpine.data('cmsImageField', () => ({
  csrf: '',
  filename: '',
  previewUrl: '',
  search: '',
  items: [],
  candidate: null,
  page: 1,
  hasMore: false,
  loading: false,
  uploading: false,
  message: '',
  pickerMessage: '',
  returnFocus: null,

  init(root) {
    this.csrf = root.dataset.csrf;
    this.filename = root.dataset.currentFilename;
    this.previewUrl = root.dataset.currentPreview;
  },

  async openPicker(button) {
    this.returnFocus = button;
    this.search = '';
    this.candidate = null;
    this.items = [];
    this.$refs.dialog.showModal();
    await this.load(1);
    this.candidate =
      this.items.find((item) => item.id === this.$refs.value.value) || null;
    this.$refs.dialog.querySelector('input[type="search"]')?.focus();
  },

  async load(page, append = false) {
    this.loading = true;
    this.pickerMessage = 'Loading media library…';
    try {
      const params = new URLSearchParams({
        search: this.search,
        page: String(page),
      });
      const response = await fetch(`/admin/media/library?${params}`, {
        credentials: 'same-origin',
        headers: { Accept: 'application/json' },
      });
      if (
        !response.ok ||
        !response.headers.get('content-type')?.includes('application/json')
      )
        throw new Error(
          'The media library could not be loaded. Reload and try again.',
        );
      const data = await response.json();
      this.items = append ? [...this.items, ...data.items] : data.items;
      if (
        this.candidate &&
        !this.items.some((item) => item.id === this.candidate.id)
      ) {
        this.candidate = null;
      }
      this.page = data.page;
      this.hasMore = data.has_more;
      this.pickerMessage = this.items.length
        ? `${this.items.length} image${this.items.length === 1 ? '' : 's'} shown.`
        : 'No images match this search.';
    } catch (error) {
      this.pickerMessage =
        error.message || 'The media library could not be loaded.';
      this.items = append ? this.items : [];
    } finally {
      this.loading = false;
    }
  },

  async upload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    this.uploading = true;
    this.message = 'Uploading image…';
    const form = new FormData();
    form.set('csrf', this.csrf);
    form.set('action', 'upload');
    form.set('upload', file);
    try {
      const response = await fetch('/admin/media?picker=1', {
        method: 'POST',
        body: form,
        credentials: 'same-origin',
        headers: { Accept: 'application/json' },
      });
      if (!response.headers.get('content-type')?.includes('application/json')) {
        throw new Error(
          'Your admin session may have expired. Reload and sign in again.',
        );
      }
      const data = await response.json();
      if (!response.ok)
        throw new Error(data.error || 'The image could not be uploaded.');
      this.apply(data.item);
      this.message = `${data.item.filename} uploaded and selected. Save or publish to apply it.`;
    } catch (error) {
      this.message = error.message || 'The image could not be uploaded.';
    } finally {
      this.uploading = false;
      event.target.value = '';
    }
  },

  apply(item) {
    this.$refs.value.value = item.id;
    this.$refs.value.dispatchEvent(new Event('input', { bubbles: true }));
    this.$refs.value.dispatchEvent(new Event('change', { bubbles: true }));
    this.filename = item.filename;
    this.previewUrl = item.preview_url;
  },

  select() {
    if (!this.candidate) return;
    this.apply(this.candidate);
    this.message = `${this.candidate.filename} selected. Save or publish to apply it.`;
    this.$refs.dialog.close();
  },

  clear() {
    this.$refs.value.value = '';
    this.$refs.value.dispatchEvent(new Event('input', { bubbles: true }));
    this.$refs.value.dispatchEvent(new Event('change', { bubbles: true }));
    this.filename = '';
    this.previewUrl = '';
    this.message =
      'Image removed from this section. Save or publish to apply the change.';
  },

  cancel() {
    this.candidate = null;
    this.$refs.dialog.close();
  },

  onClose() {
    this.candidate = null;
    this.returnFocus?.focus();
  },

  metadata(item) {
    const size = `${Math.max(1, Math.round(item.size / 1024))} KB`;
    return item.width && item.height
      ? `${item.width} × ${item.height} px · ${size}`
      : size;
  },
}));
Alpine.start();
