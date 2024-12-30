import os
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
KUBERNETES_KEY = os.environ.get('KUBERNETES_KEY', 'k8s_key')
KUBERNETES_URL = os.environ.get('KUBENETES_URL', 'https://kubernetes.default.svc.cluster.local')

PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH', 'public.pem')

