from django.shortcuts import render
import random

# Create your views here.
quotes = [
    "Optimism is a strategy for making a better future. Because unless you believe that the future can be better, you are unlikely to step up and take responsibility for making it so.",
    "If we don't believe in freedom of expression for people we despise, we don't believe in it at all.",
    "Changes and progress very rarely are gifts from above. They come out of struggles from below.",
    "There are very few people who are going to look into the mirror and say, 'That person I see is a savage monster;' instead, they make up some construction that justifies what they do.",
    "If we choose, we can live in a world of comforting illusion.",
    "I was never aware of any other option but to question everything.",
    "For the powerful, crimes are those that others commit."
]

images = [
    "chomskyimage1.jpg",
    "chomskyimage2.webp",
    "chomskyimage3.webp",
    "chomskyimage4.webp",
    "chomskyimage5.jpg"
]

def quote_of_the_day(request):

    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)

    return render(request, 'quotes/quote.html', {'quote': selected_quote, 'image': selected_image})

def show_all(request):
    return render(request, 'quotes/show_all.html', {'quotes': quotes, 'images': images})

def about(request):
    person_info = {
        'name': 'Noam Chomsky',
        'bio': 'Noam Chomsky is a renowned American linguist, philosopher, cognitive scientist, historian, social critic, and political activist. Chomsky is widely regarded as the "father of modern linguistics" due to his groundbreaking work in the field, particularly his development of the theory of generative grammar. He is also a prominent figure in cognitive science and has made significant contributions to the philosophy of language and mind. Beyond academia, Chomsky is known for his outspoken political activism, particularly his critiques of U.S. foreign policy and media. He has authored numerous books on both linguistic theory and political issues.',
        'creator': 'This web page was created by Asad Soomro, a senior undergraduate student at Boston University'
    }
    return render(request, 'quotes/about.html', {'person': person_info})