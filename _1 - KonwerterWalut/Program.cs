using System.Globalization;
using System.Xml.Linq;

namespace KonwerterWalut;

internal static class Program
{
    private static async Task Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        Console.WriteLine("[=== KONWERTER WALUT ===]");
        Console.WriteLine("Kursy NBP. Kwoty przeliczane są przez PLN\n");

        Dictionary<string, Currency> currencies;
        try
        {
            currencies = await NbpRateProvider.DownloadRatesAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Nie udało się pobrać kursów NBP: {ex.Message}");
            Console.WriteLine("Sprawdź połączenie z internetem i uruchom program ponownie");
            return;
        }

        currencies["PLN"] = new Currency("PLN", "polski złoty", 1m);
        Console.WriteLine($"Pobrano kursy dla {currencies.Count} walut");
        PrintCurrencies(currencies);
        Console.WriteLine();
        //Console.WriteLine("\"KURSY\", aby wyświetlić dostępne kody walut.\n");

        while (true)
        {
            Console.Write("Waluta źródłowa lub \"Q\"(zakończenie): ");
            string? userInput = Console.ReadLine()?.Trim().ToUpper();

            if (userInput is null) continue;

            if(userInput == "Q") break;

            if (!currencies.TryGetValue(userInput, out Currency? source))
            {
                Console.WriteLine("Nieznany kod waluty\n");
                continue;
            }

            Console.Write("Kwota do przeliczenia: ");
            string? amountText = Console.ReadLine();
            if (!TryParseAmount(amountText, out decimal amount) || amount <= 0)
            {
                Console.WriteLine("Kwota musi być poprawną liczbą większą od zera\n");
                continue;
            }

            string? targetCode;

            getTargetCode:
            Console.Write("Waluta docelowa: ");
            targetCode = Console.ReadLine()?.Trim().ToUpperInvariant();

            if (!currencies.TryGetValue(targetCode, out Currency? target))
            {
                Console.WriteLine("Nieznany kod waluty\n");
                goto getTargetCode;
            }
            else if(source == target)
            {
                Console.WriteLine("Waluta startowa i docelowa jest identyczna\n");
                goto getTargetCode;
            }
            decimal result = amount * source.RateInPln / target.RateInPln;
            Console.WriteLine($"\n{amount.ToString().Replace(",",".")} {source.Code} = " + $"{result.ToString().Replace(",", ".")} {target.Code}");
            Console.WriteLine($"Kurs {source.Code}: {source.RateInPln.ToString().Replace(",", ".")} PLN");
            Console.WriteLine($"Kurs {target.Code}: {target.RateInPln.ToString().Replace(",", ".")} PLN");
        }

        Console.WriteLine("Koniec");
    }

    private static bool TryParseAmount(string? input, out decimal amount)
    {
        amount = 0;
        if (string.IsNullOrWhiteSpace(input)) return false;

        return decimal.TryParse(input.Trim().Replace(',', '.'), NumberStyles.AllowDecimalPoint | NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out amount);
    }

    private static void PrintCurrencies(Dictionary<string, Currency> currencies)
    {
        Console.WriteLine("\nDostępne waluty:");
        foreach (Currency currency in currencies.Values.OrderBy(c => c.Code)) Console.WriteLine($"{currency.Code,-5} {currency.Name}");
    }
}

internal sealed record Currency(string Code, string Name, decimal RateInPln);

internal static class NbpRateProvider
{
    public static async Task<Dictionary<string, Currency>> DownloadRatesAsync()
    {
        const string url = "https://static.nbp.pl/dane/kursy/xml/LastA.xml";

        using var client = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(15)
        };

        string xml = await client.GetStringAsync(url);

        XDocument document;
        try
        {
            document = XDocument.Parse(xml);
        }
        catch (System.Xml.XmlException ex)
        {

            string fragment = xml.Length > 100 ? xml[..100] : xml;

            throw new InvalidDataException($"Nie usało się przeparsować na XML: {ex.Message}\n" + $"Odpowiedzi serwera:\n{fragment}", ex);
        }

        var currencies = new Dictionary<string, Currency>(StringComparer.OrdinalIgnoreCase);

        foreach (XElement item in document.Descendants("pozycja"))
        {
            string? code = item.Element("kod_waluty")?.Value.Trim();

            string? name = item.Element("nazwa_waluty")?.Value.Trim();

            string? rateText = item.Element("kurs_sredni")?.Value.Trim();

            if (string.IsNullOrWhiteSpace(code) || string.IsNullOrWhiteSpace(name) || string.IsNullOrWhiteSpace(rateText))
            {
                continue;
            }

            if (decimal.TryParse(rateText, NumberStyles.Number, CultureInfo.GetCultureInfo("pl-PL"), out decimal rate) && rate > 0)
            {
                currencies[code] = new Currency(code, name, rate);
            }
        }

        if (currencies.Count == 0)
        {
            throw new InvalidDataException( "XML nie zawiera walut");
        }

        return currencies;
    }
}
