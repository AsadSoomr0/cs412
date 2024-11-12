from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.db.models import Count
from .models import *
import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100 

    def get_queryset(self):
        queryset = super().get_queryset()

        def parse_boolean(value):
            if value == 'TRUE':
                return True
            elif value == 'FALSE':
                return False
            return None

        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = parse_boolean(self.request.GET.get('v20state'))
        v21town = parse_boolean(self.request.GET.get('v21town'))
        v21primary = parse_boolean(self.request.GET.get('v21primary'))
        v22general = parse_boolean(self.request.GET.get('v22general'))
        v23town = parse_boolean(self.request.GET.get('v23town'))

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state:
            queryset = queryset.filter(v20state=v20state)
        if v21town:
            queryset = queryset.filter(v21town=v21town)
        if v21primary:
            queryset = queryset.filter(v21primary=v21primary)
        if v22general:
            queryset = queryset.filter(v22general=v22general)
        if v23town:
            queryset = queryset.filter(v23town=v23town)

        return queryset
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        def parse_boolean(value):
            return value.lower() == 'true' if value else None
        
        queryset = super().get_queryset()
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Boolean fields for election participation
        v20state = parse_boolean(self.request.GET.get('v20state'))
        v21town = parse_boolean(self.request.GET.get('v21town'))
        v21primary = parse_boolean(self.request.GET.get('v21primary'))
        v22general = parse_boolean(self.request.GET.get('v22general'))
        v23town = parse_boolean(self.request.GET.get('v23town'))

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state is not None:
            queryset = queryset.filter(v20state=v20state)
        if v21town is not None:
            queryset = queryset.filter(v21town=v21town)
        if v21primary is not None:
            queryset = queryset.filter(v21primary=v21primary)
        if v22general is not None:
            queryset = queryset.filter(v22general=v22general)
        if v23town is not None:
            queryset = queryset.filter(v23town=v23town)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate the Birth Year Distribution histogram
        birth_years = self.get_queryset().values_list('date_of_birth', flat=True)
        birth_year_counts = {}
        for birth_year in birth_years:
            year = birth_year.year
            if year not in birth_year_counts:
                birth_year_counts[year] = 0
            birth_year_counts[year] += 1

        birth_year_chart = go.Figure(
            data=[go.Bar(x=list(birth_year_counts.keys()), y=list(birth_year_counts.values()))]
        )
        birth_year_chart.update_layout(title='Birth Year Distribution')
        context['birth_year_chart'] = birth_year_chart.to_html(full_html=False)

        # Generate the Party Affiliation Pie Chart
        party_counts = self.get_queryset().values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_labels = [entry['party_affiliation'] for entry in party_counts]
        party_values = [entry['count'] for entry in party_counts]

        party_chart = go.Figure(
            data=[go.Pie(labels=party_labels, values=party_values)]
        )
        party_chart.update_layout(title='Party Affiliation Distribution')
        context['party_chart'] = party_chart.to_html(full_html=False)

        # Generate the Voter Participation by Election histogram
        election_counts = {
            '2020 State': self.get_queryset().filter(v20state=True).count(),
            '2021 Town': self.get_queryset().filter(v21town=True).count(),
            '2021 Primary': self.get_queryset().filter(v21primary=True).count(),
            '2022 General': self.get_queryset().filter(v22general=True).count(),
            '2023 Town': self.get_queryset().filter(v23town=True).count(),
        }

        election_chart = go.Figure(
            data=[go.Bar(x=list(election_counts.keys()), y=list(election_counts.values()))]
        )
        election_chart.update_layout(title='Voter Participation by Election')
        context['election_chart'] = election_chart.to_html(full_html=False)

        return context