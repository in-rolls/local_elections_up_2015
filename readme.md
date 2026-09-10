# UP 2015 winner lists have moved

This collection is maintained in
[in-rolls/local_elections_up](https://github.com/in-rolls/local_elections_up).
That state repository owns the original source files, collection and parsing
tools, and standardized Uttar Pradesh election datasets.

- [Original 2015 CSVs, provenance, and citation](https://github.com/in-rolls/local_elections_up/tree/main/data/raw/2015/winner_lists)
- [Derived Parquet tables](https://github.com/in-rolls/local_elections_up/tree/main/data/interim/winner_lists_2015)
- [Converter](https://github.com/in-rolls/local_elections_up/blob/main/scripts/convert_winner_lists_2015.py)

All 226 original CSVs and 140,709 records are preserved in the consolidated
collection. Its authors are Suriyan Laohaprapanon and Gaurav Sood. This repository
retains the original collection history for provenance. Submit new work and
issues to `local_elections_up`.

## Original collection notes

### 2015 UP Panchayat General Election Results

We scraped 2015 UP Panchayat General Election Results posted at [UP State Election Commission](http://sec.up.nic.in/ElecLive/WinnerList.aspx).

The website offers two dropdowns (one for district, one for post) through which all the results are accessible.

Type of posts = Area panchayat chief, district panchayat president, district panchayat member, area panchayat member, gram panchayat head.

For area panchayat chief and district panchayat president, there is only have one file each.

### Script

[Original collection notebook](https://github.com/in-rolls/local_elections_up_2015/blob/789462339f5661aa31dd4c05c56bce5f46b5bb94/scripts/WinnerList.ipynb)

### Data

[Data](data/)

The data format varies slightly by post.

For area panchayat chief, the header =

```District, Kshetra Panchayat,	Reservation of post,	Candidate	Father / husband,	Candidate's reservation,	educational qualification,	Gender,	Mobile number,	Received valid vote,	Votes received,	vote %,	result```

For district panchayat president, the header =

```District Panchayat,	Reservation of post,	Candidate	Father / husband, Candidate's reservation,	educational qualification,	Gender, Mobile number, Received valid vote, Votes received, vote %, result```

For district panchayat member, the header =

```District Panchayat Ward,	Reservation of post,	Candidate	Father / husband,	Candidate's reservation,	educational qualification,	Gender,	Mobile number,	Received valid vote,	Votes received,	vote %,	result```

For area panchayat member, the header =

```The block, Kshetra Panchayat Ward,	Reservation of post, Candidate	Father / husband, Candidate's reservation, educational qualification,	Gender,	Mobile number,	Received valid vote,	Votes received,	vote %, result```

For gram panchayat head, the header =

```The block,	Village Panchayat,	Reservation of post,	Candidate	Father / husband,	Candidate's reservation,	educational qualification,	Gender,	Mobile number,	Received valid vote,	Votes received	vote %,	result```
