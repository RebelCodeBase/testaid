import testaid


def test_testaid_debug(host, moleculebook):
    playbook = moleculebook.get()
    args = dict(path='/tmp/moleculebook_did_this', state='touch')
    task_touch = dict(action=dict(module='file', args=args))
    playbook['tasks'].append(task_touch)
    moleculebook.set(playbook)
    moleculebook.run()
    assert host.file('/tmp/moleculebook_did_this').exists
