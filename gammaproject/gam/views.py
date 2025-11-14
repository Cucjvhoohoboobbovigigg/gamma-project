from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
model = Poll
template_name = 'polls/poll_detail.html'

@method_decorator(login_required, name='dispatch')
class PollResultsView(generic.DetailView):
model = Poll
template_name = 'polls/poll_results.html'

@login_required
def poll_create(request):
ChoiceFormSet = formset_factory(forms.Form, extra=2)
if request.method == 'POST':
form = PollForm(request.POST)
choices = request.POST.getlist('choice')
if form.is_valid() and len([c for c in choices if c.strip()]) >= 2:
poll = form.save(commit=False)
poll.created_by = request.user
poll.save()
for choice_text in choices:
if choice_text.strip():
Choice.objects.create(poll=poll, text=choice_text.strip())
messages.success(request, 'Poll created successfully')
return redirect('polls:detail', pk=poll.pk)
else:
messages.error(request, 'Please provide a question and at least two choices.')
else:
form = PollForm()
return render(request, 'polls/poll_create.html', {'form': form})

@login_required
def vote(request, pk):
poll = get_object_or_404(Poll, pk=pk)
choice_id = request.POST.get('choice')
if not choice_id:
messages.error(request, 'You must select a choice.')
return redirect('polls:detail', pk=pk)
choice = get_object_or_404(Choice, pk=choice_id, poll=poll)

# prevent double-voting via unique_together + try/except
try:
Vote.objects.create(poll=poll, choice=choice, user=request.user)
except Exception:
messages.error(request, 'You have already voted in this poll.')
return redirect('polls:results', pk=pk)

messages.success(request, 'Thanks for voting!')
return redirect('polls:results', pk=p