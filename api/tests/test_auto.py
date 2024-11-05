import unittest

from parameterized import parameterized

from api.auto import assume_tags

class TestAuto(unittest.TestCase):

    @parameterized.expand([
        ['abcdefg 2024-10-08 10_56 [abcdefg].mp4', '1729150390.4448655', ['abcdefg', '2024', '2024-10-08']],
        ['zzzzzzaaa 2024-04-19 10_56 [zzzzzzaaa].mp4', '1714033635.9538631', ['zzzzzzaaa', '2024', '2024-04-19']],
        ['cats/cats 2023-04-19 15_28-cats.mp4', '1709785458.657367', ['cats', '2023', '2023-04-19']],
        ['dog/dogs 2020-09-27 08_42-dogs.mp4', '1709782471.7099986', ['2020-09-27', '2020', 'dog', 'dogs']],
        # this one is rubbish and broken
        #['motion/0-01-20230331153612.mkv', '1709782149.3173475', ['motion', '2023-03-31']],
        ['scans/scans 2021-02-09 17_08-scans.mp4', '1709777931.2136106', ['scans', '2021', '2021-02-09']],
        ['lonelyday/lonelyday_ 2020-03-26 20_54-lonelyday_.mp4', '1709777376.9182405', ['lonelyday', 'lonelyday_', '2020', '2020-03-26']],
        ['_Favourites/Fast Cars/2019-07-29 23-52-49.mkv', '1709772090.3415468', ['Fast', 'Cars', 'Favourites', '2019', '2019-07-29']],
        ['Unsorted/SheSellsSeashells_By-the-Sea-Shore.mp4', '1709771705.9740956', ['SheSellsSeashells_By-the-Sea-Shore', 'Unsorted', '2024', '2024-03-07']],
        ['MKV/2020-08-09 01-06-57.mkv', '1709770320.9260023', ['MKV', '2020-08-09', '2020']],
        ['Offspring/KeepEmSeperated-20230505.mp4', '1709770320.9260023', ['2023', '2023-05-05', 'KeepEmSeperated-', 'Offspring']]
    ])
    def test_assumed_tags_are_reasonable(self, relative_path, created, expected_tags):
        
        # arrange
        video = {
            'relative_path': relative_path,
            'created': created
        }

        # act
        actual_tags = assume_tags(video)

        # assert
        self.assertCountEqual(set(expected_tags), set(actual_tags))
